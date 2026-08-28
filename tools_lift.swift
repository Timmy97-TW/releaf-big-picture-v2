import Foundation
import Vision
import CoreImage
import AppKit

// lift <in> <out.png> [--all|--largest]
let args = CommandLine.arguments
guard args.count >= 3 else { FileHandle.standardError.write("usage: lift in out [--all]\n".data(using:.utf8)!); exit(2) }
let inURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
let useAll = args.contains("--all")

guard let src = CIImage(contentsOf: inURL) else { print("ERR load"); exit(1) }
let handler = VNImageRequestHandler(ciImage: src, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
do { try handler.perform([req]) } catch { print("ERR perform \(error)"); exit(1) }
guard let obs = req.results?.first else { print("ERR no-subject"); exit(3) }

let instances: IndexSet = useAll ? obs.allInstances : obs.allInstances
do {
  let buf = try obs.generateMaskedImage(ofInstances: instances, from: handler, croppedToInstancesExtent: true)
  let ci = CIImage(cvPixelBuffer: buf)
  let ctx = CIContext()
  guard let cg = ctx.createCGImage(ci, from: ci.extent) else { print("ERR cg"); exit(1) }
  let rep = NSBitmapImageRep(cgImage: cg)
  guard let data = rep.representation(using: .png, properties: [:]) else { print("ERR png"); exit(1) }
  try data.write(to: outURL)
  print("OK \(Int(ci.extent.width))x\(Int(ci.extent.height)) instances=\(obs.allInstances.count)")
} catch { print("ERR mask \(error)"); exit(1) }
