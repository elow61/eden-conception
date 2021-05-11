import * as three from 'https://cdn.skypack.dev/pin/three@v0.128.0-4xvsPydvGvI2Nx1Gbe39/mode=imports,min/optimized/three.js';
import { OrbitControls } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/controls/OrbitControls.js';

const textureLoader = new three.TextureLoader();
const circleTexture = textureLoader.load('/static/img/circle.png')

// Create the scene
const scene = new three.Scene();
const count = 9;
const distance = 2;

scene.add(new three.AxesHelper());

// Create the camera
const camera = new three.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.001, 1000);
camera.position.z = 2;
camera.position.y = 0.5;
camera.position.x = 0.5;
scene.add(camera);

// Create the points
const points = new Float32Array(count * 3);
for (let i=0; i < points.length; i++) {
    points[i] = three.MathUtils.randFloatSpread(distance * 2);
}

// Create a cube
const geometry = new three.BufferGeometry();
geometry.setAttribute('position', new three.Float32BufferAttribute(points, 3))
const pointMaterial = new three.PointsMaterial({
    size: .6,
    map: circleTexture,
    alphaTest: 0.02,
    transparent: true,
})
const pointsObject = new three.Points(geometry, pointMaterial);
const group = new three.Group();
group.add(pointsObject);

scene.add(group);
// Create the renderer for view in website
const renderer = new three.WebGLRenderer({
    antialias: true,
    alpha: true,
});
renderer.setClearColor(0x000000, 0);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
const header = document.querySelector('header');
header.insertBefore(renderer.domElement, header.firstChild);
renderer.render(scene, camera);

// This controls can move the element with the mouse
const controls = new OrbitControls(camera, renderer.domElement);
const clock = new three.Clock();

// let mouseX = 0;
// window.addEventListener('mousemove', e => {
//     mouseX = e.clientX;
// })

// Animation function
function tick() {
    const time = clock.getElapsedTime();
    group.rotation.y = time * 0.1;
    group.rotation.x = time * 0.1;
    renderer.render(scene, camera);
    // camera.position.x -= 0.01; 
    // camera.lookAt(0, 0, 0);
    controls.update();
    requestAnimationFrame(tick);
    // const ratio = (mouseX / window.innerWidth - 0.5) * 2;
    // group.rotation.x = ratio * Math.PI * 1;
}

tick()

// Update the scene if the user resize the window
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
})

