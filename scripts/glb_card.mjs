// Render one or more GLB models (props/) into a transparent PNG with the channel's ink outline,
// so it can become a movable "prop puppet" card (a ship that sails and sinks, a castle that sinks...).
// Static props in short.json cannot move, puppets can.
//   node scripts/glb_card.mjs spec.json out.png
// spec.json: {"size": [1400, 1000], "yaw": 25, "pitch": 6, "ink": 5,
//             "parts": [{"file": "props/kenney_pirate-kit/ship-pirate-large.glb", "pos": [0,0,0], "scale": 1, "rotY": 0}]}
// Orthographic camera, auto-framed, cropped to the content. Writes out.png (and prints its size + world size).
import http from 'http'; import fs from 'fs'; import path from 'path'; import { createRequire } from 'module'; import { fileURLToPath } from 'url'; import { execFileSync } from 'child_process';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ST = path.join(ROOT, '.claude/skills/ricksclips-short-style/scripts/stage');
const { chromium } = createRequire(ST + '/render.mjs')('playwright');
const spec = JSON.parse(fs.readFileSync(process.argv[2])), out = path.resolve(process.argv[3]);
const page_html = `<!doctype html><script type="importmap">{"imports":{"three":"/three/build/three.module.js","three/addons/":"/three/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three'; import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
window.go = async (S) => {
  const [W, H] = S.size || [1400, 1000], r = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  r.setSize(W, H); r.setClearColor(0, 0); const sc = new THREE.Scene(), L = new GLTFLoader(), g = new THREE.Group(); sc.add(g);
  for (const p of S.parts) { const m = (await L.loadAsync('/' + p.file)).scene; m.position.set(...(p.pos || [0,0,0])); m.scale.setScalar(p.scale || 1); m.rotation.y = (p.rotY || 0) * Math.PI / 180; g.add(m); }
  const sun = new THREE.DirectionalLight('#ffe8c8', 2.6); sun.position.set(4, 6, 6); sc.add(sun); sc.add(new THREE.HemisphereLight('#c8ccff', '#8a5a86', 1.7));
  const yaw = (S.yaw || 0) * Math.PI / 180, pit = (S.pitch || 0) * Math.PI / 180, dir = new THREE.Vector3(Math.sin(yaw) * Math.cos(pit), Math.sin(pit), Math.cos(yaw) * Math.cos(pit));
  sc.updateMatrixWorld(true); const b = new THREE.Box3().setFromObject(g), c = b.getCenter(new THREE.Vector3()), cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 500);
  cam.position.copy(c).addScaledVector(dir, 100); cam.lookAt(c); cam.updateMatrixWorld(); const inv = cam.matrixWorldInverse; let x = 0, y = 0;
  for (let i = 0; i < 8; i++) { const v = new THREE.Vector3(i & 1 ? b.max.x : b.min.x, i & 2 ? b.max.y : b.min.y, i & 4 ? b.max.z : b.min.z).applyMatrix4(inv); x = Math.max(x, Math.abs(v.x)); y = Math.max(y, Math.abs(v.y)); }
  const k = Math.max(x / W, y / H) * 1.06; cam.left = -k * W; cam.right = k * W; cam.top = k * H; cam.bottom = -k * H; cam.updateProjectionMatrix();
  r.outputColorSpace = THREE.SRGBColorSpace; r.render(sc, cam); const col = r.domElement.toDataURL();
  sc.overrideMaterial = new THREE.MeshNormalMaterial({ side: THREE.DoubleSide }); r.render(sc, cam); const nor = r.domElement.toDataURL();
  return { col, nor, upp: 2 * k };
};</script>`;
const mime = { '.js': 'text/javascript', '.glb': 'model/gltf-binary', '.png': 'image/png' };
const srv = http.createServer((q, s) => {
  const u = decodeURIComponent(q.url.split('?')[0]); if (u === '/') { s.setHeader('content-type', 'text/html'); return s.end(page_html); }
  const f = u.startsWith('/three/') ? path.join(ST, 'node_modules', u) : path.join(ROOT, u);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { s.statusCode = 404; return s.end(); }
  s.setHeader('content-type', mime[path.extname(f)] || 'application/octet-stream'); fs.createReadStream(f).pipe(s);
}).listen(0, '127.0.0.1');
await new Promise(r => srv.on('listening', r));
let br; try { br = await chromium.launch({ channel: 'chrome' }); } catch { br = await chromium.launch(); }
const pg = await br.newPage(); pg.on('pageerror', e => console.error(String(e)));
await pg.goto(`http://127.0.0.1:${srv.address().port}/`); await pg.waitForFunction('window.go');
const res = await pg.evaluate(S => window.go(S), spec); await br.close(); srv.close();
for (const n of ['col', 'nor']) fs.writeFileSync(`${out}.${n}.png`, Buffer.from(res[n].split(',')[1], 'base64'));
execFileSync(path.join(ROOT, '.venv/bin/python'), ['-c', `
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
o, ink, upp = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
c = np.array(Image.open(o + '.col.png').convert('RGBA')).astype(float); n = np.array(Image.open(o + '.nor.png').convert('RGBA')).astype(float)
e = np.zeros(c.shape[:2])
for ax in (0, 1): e = np.maximum(e, np.abs(np.diff(n, axis=ax, append=np.take(n, [-1], axis=ax))).max(axis=2))
inner = nd.binary_dilation(e > 55, iterations=max(1, ink // 3))
a = c[..., 3] > 100; ring = nd.binary_dilation(a, iterations=ink) & ~nd.binary_erosion(a, iterations=1)
m = nd.gaussian_filter((ring | (inner & a)).astype(float), 0.8)[..., None]
al = np.maximum(c[..., 3] / 255, nd.gaussian_filter(ring.astype(float), 0.8))
rgb = c[..., :3] * (1 - m) + np.array([39, 25, 37]) * m
im = Image.fromarray(np.dstack([rgb, al * 255]).clip(0, 255).astype('uint8')); im = im.crop(im.getbbox()); im.save(o)
print(o, im.size, 'world size', round(im.width * upp, 2), 'x', round(im.height * upp, 2))
`, out, String(spec.ink || 5), String(res.upp)], { stdio: 'inherit' });
for (const n of ['col', 'nor']) fs.unlinkSync(`${out}.${n}.png`);
