import AppKit
import WebKit

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var window: NSWindow!
    private var bridge: Process?

    func applicationDidFinishLaunching(_ notification: Notification) {
        let executable = Bundle.main.resourceURL!.appendingPathComponent("bridge/PromptMaster")
        let process = Process()
        process.executableURL = executable
        process.environment = ProcessInfo.processInfo.environment.merging(["PROMPT_MASTER_NO_BROWSER": "1"]) { _, new in new }
        do {
            try process.run()
            bridge = process
        } catch {
            NSAlert(error: error).runModal()
            NSApp.terminate(nil)
            return
        }

        window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 1440, height: 900),
                          styleMask: [.titled, .closable, .miniaturizable, .resizable],
                          backing: .buffered, defer: false)
        window.title = "Prompt Master"
        window.minSize = NSSize(width: 900, height: 650)
        let view = WKWebView(frame: window.contentView!.bounds)
        view.autoresizingMask = [.width, .height]
        window.contentView = view
        window.center()
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        loadWhenReady(view, attempts: 40)
    }

    private func loadWhenReady(_ view: WKWebView, attempts: Int) {
        guard attempts > 0 else { return }
        let url = URL(string: "http://127.0.0.1:8080/")!
        URLSession.shared.dataTask(with: url) { _, response, _ in
            DispatchQueue.main.async {
                if let http = response as? HTTPURLResponse, http.statusCode == 200 {
                    view.load(URLRequest(url: url))
                } else {
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
                        self.loadWhenReady(view, attempts: attempts - 1)
                    }
                }
            }
        }.resume()
    }

    func applicationWillTerminate(_ notification: Notification) {
        bridge?.terminate()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()
