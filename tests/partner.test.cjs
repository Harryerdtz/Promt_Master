const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const source = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const builders = source.slice(source.indexOf('function buildPositivePrompt('), source.indexOf('function updatePromptOutputs('));
const partnerStart = source.indexOf('/* Partner-Tags bleiben unabhängig');
const partnerLogic = source.slice(partnerStart, source.indexOf('\ninit();', partnerStart));
assert(partnerStart > 0 && builders.includes('function buildNegativePrompt('));

function prompts(changes = {}) {
  const state = {
    model: 'pony', styleMode: 'anime', tags: [], extras: [], custom: [], manual: '',
    negCustom: '', negExtras: [], loras: [], weights: {}, partnerMode: 'hetero', partnerFaceless: false,
    partnerTags: [], partnerOff: [], ...changes
  };
  const context = vm.createContext({
    state,
    MODELS: { pony: { prefix: '', extras: {}, negative: 'lowres', neg: [] } },
    commaList: value => String(value || '').split(',').map(part => part.trim()).filter(Boolean),
    uniq: items => [...new Set(items)]
  });
  vm.runInContext(`${builders}\n${partnerLogic}`, context);
  return {
    positive: vm.runInContext('buildPositivePrompt(false)', context).split(', '),
    negative: vm.runInContext('buildNegativePrompt()', context).split(', ')
  };
}

test('Frau und Mann ersetzen widersprüchliche Personen-Tags', () => {
  const { positive, negative } = prompts({ tags: ['kissing', '2girls', 'solo'], negCustom: '1boy' });
  for (const tag of ['1girl', '1boy', 'hetero']) assert(positive.includes(tag));
  for (const tag of ['2girls', 'solo']) assert(!positive.includes(tag));
  assert(negative.includes('2girls'));
  assert(!negative.includes('1boy'));
});

test('zwei Frauen und zwei Männer funktionieren auch mit manuellen Tags', () => {
  const women = prompts({ partnerMode: 'yuri', custom: ['adult kissing'], tags: ['1boy'] });
  assert(women.positive.includes('2girls') && women.positive.includes('yuri'));
  assert(!women.positive.includes('1boy'));
  assert(women.negative.includes('1boy'));

  const men = prompts({ partnerMode: 'yaoi', manual: 'holding hands, 1girl' });
  assert(men.positive.includes('2boys') && men.positive.includes('yaoi'));
  assert(!men.positive.includes('1girl'));
  assert(men.negative.includes('1girl'));
});

test('Einzelpersonen und Abschaltung ergänzen keinen Partner', () => {
  assert(!prompts({ tags: ['self touch'] }).positive.includes('1boy'));
  assert(!prompts({ tags: ['kissing'], partnerMode: 'off' }).positive.includes('1boy'));
  assert(!prompts({ tags: ['kissing'], partnerOff: ['kissing'] }).positive.includes('1boy'));
});

test('eigene Partner-Markierungen und Gruppen-Tags werden erkannt', () => {
  assert(prompts({ tags: ['custom duo'], partnerTags: ['custom duo'] }).positive.includes('1boy'));
  assert(prompts({ tags: ['threesome'] }).positive.includes('multiple boys'));
});

test('Presets speichern und laden die Partner-Auswahl', () => {
  const presetLogic = source.slice(source.indexOf('function savePreset()'), source.indexOf('function deletePreset('));
  const fields = new Map();
  const field = id => fields.get(id) || (fields.set(id, { value: '' }), fields.get(id));
  const state = {
    presets: [], model: 'pony', styleMode: 'anime', tags: ['kissing'], extras: [], custom: [],
    manual: '', negCustom: '', generation: {}, loras: [], partnerMode: 'yaoi',
    partnerFaceless: false, partnerTags: ['custom duo'], partnerOff: ['hugging']
  };
  field('#presetName').value = 'Zwei Männer';
  const context = vm.createContext({
    state, crypto: require('node:crypto').webcrypto, Date, Map,
    $: field, document: { getElementById: field },
    buildPositivePrompt: () => '2boys, yaoi, kissing',
    renderPresets() {}, saveState() {}, loadLibraryView() {}, showToast() {},
    renderLoras() {}, renderModels() {}, renderStyleSwitch() {}, renderExtras() {},
    renderCustomChips() {}, syncRandomizerControls() {}, updatePromptOutputs() {}
  });
  vm.runInContext(presetLogic, context);
  vm.runInContext('savePreset()', context);
  const saved = state.presets[0];
  assert.equal(saved.partnerMode, 'yaoi');
  assert.deepEqual([...saved.partnerTags], ['custom duo']);
  state.partnerMode = 'hetero';
  state.partnerTags = [];
  vm.runInContext('loadPreset(state.presets[0])', context);
  assert.equal(state.partnerMode, 'yaoi');
  assert.deepEqual([...state.partnerTags], ['custom duo']);
});
