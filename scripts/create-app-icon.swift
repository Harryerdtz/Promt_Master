import AppKit

let size = 1024
let output = CommandLine.arguments[1]
let image = NSBitmapImageRep(
    bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size,
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true,
    isPlanar: false, colorSpaceName: .deviceRGB,
    bytesPerRow: 0, bitsPerPixel: 0
)!
let context = NSGraphicsContext(bitmapImageRep: image)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = context
context.imageInterpolation = .high

func color(_ hex: UInt32) -> NSColor {
    NSColor(
        calibratedRed: CGFloat((hex >> 16) & 255) / 255,
        green: CGFloat((hex >> 8) & 255) / 255,
        blue: CGFloat(hex & 255) / 255,
        alpha: 1
    )
}

func rounded(_ rect: NSRect, radius: CGFloat, fill: UInt32, stroke: UInt32? = nil, lineWidth: CGFloat = 1) {
    let path = NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius)
    color(fill).setFill()
    path.fill()
    if let stroke {
        color(stroke).setStroke()
        path.lineWidth = lineWidth
        path.stroke()
    }
}

NSColor.clear.setFill()
NSRect(x: 0, y: 0, width: size, height: size).fill()
rounded(NSRect(x: 32, y: 32, width: 960, height: 960), radius: 210, fill: 0x0d1117, stroke: 0x30363d, lineWidth: 10)
rounded(NSRect(x: 140, y: 184, width: 744, height: 656), radius: 92, fill: 0x161b22, stroke: 0x30363d, lineWidth: 10)

for (x, hex) in [(208.0, 0xf85149), (280.0, 0x3fb950), (352.0, 0x2f81f7)] {
    color(UInt32(hex)).setFill()
    NSBezierPath(ovalIn: NSRect(x: x, y: 752, width: 36, height: 36)).fill()
}

let prompt = NSBezierPath()
prompt.move(to: NSPoint(x: 270, y: 623))
prompt.line(to: NSPoint(x: 432, y: 512))
prompt.line(to: NSPoint(x: 270, y: 401))
prompt.lineWidth = 56
prompt.lineCapStyle = .round
prompt.lineJoinStyle = .round
color(0x2f81f7).setStroke()
prompt.stroke()

rounded(NSRect(x: 494, y: 483, width: 244, height: 58), radius: 27, fill: 0x3fb950)
rounded(NSRect(x: 494, y: 374, width: 154, height: 30), radius: 15, fill: 0x8b949e)

context.flushGraphics()
NSGraphicsContext.restoreGraphicsState()
let data = image.representation(using: .png, properties: [:])!
try data.write(to: URL(fileURLWithPath: output))
