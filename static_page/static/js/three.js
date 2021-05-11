import * as t from 'https://cdn.skypack.dev/pin/three@v0.128.0-4xvsPydvGvI2Nx1Gbe39/mode=imports,min/optimized/three.js';


let group;
let container;
const particlesData = [];
let camera, scene, renderer;
let positions, colors;
let particles;
let pointCloud;
let particlePositions;
let linesMesh;

const maxParticleCount = 500;
let particleCount = 280;
const r = 800;
const rHalf = r / 2;

const effectController = {
    showDots: true,
    showLines: true,
    minDistance: 90,
    limitConnections: false,
    maxConnections: 20,
    particleCount: 280
};

init();
animate();

function init() {
    container = document.querySelector('header');

    camera = new t.PerspectiveCamera(12, window.innerWidth / window.innerHeight, 1, 4000);
    camera.position.z = 1750;

    scene = new t.Scene();

    group = new t.Group();
    scene.add(group);

    const segments = maxParticleCount * maxParticleCount;

    positions = new Float32Array(segments * 3);
    colors = new Float32Array(segments * 3);

    const pMaterial = new t.PointsMaterial({
        color: 0xFFFFFF,
        size: 3,
        blending: t.AdditiveBlending,
        transparent: true,
        sizeAttenuation: false,
    });

    particles = new t.BufferGeometry();
    particlePositions = new Float32Array(maxParticleCount * 3);

    for (let i=0; i < maxParticleCount; i++) {

        const x = Math.random() * r - r / 2;
        const y = Math.random() * r - r / 2;
        const z = Math.random() * r - r / 2;

        particlePositions[i * 3] = x;
        particlePositions[i * 3 + 1] = y;
        particlePositions[i * 3 + 2] = z;

        // Add it to the BoxGeometry
        const velocity = - 1 + Math.random() * 2
        particlesData.push({
            velocity: new t.Vector3(velocity, velocity, velocity),
            numConnections: 0,
        })

    }

    particles.setDrawRange(0, particleCount);
    particles.setAttribute('position', new t.BufferAttribute(particlePositions, 3).setUsage(t.DynamicDrawUsage));

    // Create the particle systems
    pointCloud = new t.Points(particles, pMaterial);
    group.add(pointCloud);

    const geometry = new t.BufferGeometry();

    geometry.setAttribute('position', new t.BufferAttribute(positions, 3).setUsage(t.DynamicDrawUsage));
    geometry.setAttribute('color', new t.BufferAttribute(colors, 3).setUsage(t.DynamicDrawUsage));
    geometry.computeBoundingSphere();
    geometry.setDrawRange(0, 0);

    const material = new t.LineBasicMaterial({
        vertexColors: true,
        blending: t.AdditiveBlending,
        transparent: true,
    });

    linesMesh = new t.LineSegments(geometry, material);
    group.add(linesMesh);

    renderer = new t.WebGLRenderer({antialias: true, alpha: true});
    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.outputEncoding = t.sRGBEncoding;

    container.insertBefore(renderer.domElement, container.firstChild);
}

function animate() {
    let vertexpos = 0;
    let colorpos = 0;
    let numConnected = 0;

    for ( let i = 0; i < particleCount; i ++ )
        particlesData[ i ].numConnections = 0;

    for ( let i = 0; i < particleCount; i ++ ) {

        // get the particle
        const particleData = particlesData[ i ];

        particlePositions[ i * 3 ] += particleData.velocity.x;
        particlePositions[ i * 3 + 1 ] += particleData.velocity.y;
        particlePositions[ i * 3 + 2 ] += particleData.velocity.z;

        if ( particlePositions[ i * 3 + 1 ] < - rHalf || particlePositions[ i * 3 + 1 ] > rHalf )
            particleData.velocity.y = - particleData.velocity.y;

        if ( particlePositions[ i * 3 ] < - rHalf || particlePositions[ i * 3 ] > rHalf )
            particleData.velocity.x = - particleData.velocity.x;

        if ( particlePositions[ i * 3 + 2 ] < - rHalf || particlePositions[ i * 3 + 2 ] > rHalf )
            particleData.velocity.z = - particleData.velocity.z;

        if ( effectController.limitConnections && particleData.numConnections >= effectController.maxConnections )
            continue;

        // Check collision
        for ( let j = i + 1; j < particleCount; j ++ ) {

            const particleDataB = particlesData[ j ];
            if ( effectController.limitConnections && particleDataB.numConnections >= effectController.maxConnections )
                continue;

            const dx = particlePositions[ i * 3 ] - particlePositions[ j * 3 ];
            const dy = particlePositions[ i * 3 + 1 ] - particlePositions[ j * 3 + 1 ];
            const dz = particlePositions[ i * 3 + 2 ] - particlePositions[ j * 3 + 2 ];
            const dist = Math.sqrt( dx * dx + dy * dy + dz * dz );

            if ( dist < effectController.minDistance ) {

                particleData.numConnections ++;
                particleDataB.numConnections ++;

                const alpha = 1.0 - dist / effectController.minDistance;

                positions[ vertexpos ++ ] = particlePositions[ i * 3 ];
                positions[ vertexpos ++ ] = particlePositions[ i * 3 + 1 ];
                positions[ vertexpos ++ ] = particlePositions[ i * 3 + 2 ];

                positions[ vertexpos ++ ] = particlePositions[ j * 3 ];
                positions[ vertexpos ++ ] = particlePositions[ j * 3 + 1 ];
                positions[ vertexpos ++ ] = particlePositions[ j * 3 + 2 ];

                colors[ colorpos ++ ] = alpha;
                colors[ colorpos ++ ] = alpha;
                colors[ colorpos ++ ] = alpha;

                colors[ colorpos ++ ] = alpha;
                colors[ colorpos ++ ] = alpha;
                colors[ colorpos ++ ] = alpha;

                numConnected ++;

            }

        }

    }


    linesMesh.geometry.setDrawRange( 0, numConnected * 2 );
    linesMesh.geometry.attributes.position.needsUpdate = true;
    linesMesh.geometry.attributes.color.needsUpdate = true;

    pointCloud.geometry.attributes.position.needsUpdate = true;

    requestAnimationFrame( animate );

    // stats.update();
    render();
}

function render() {

    const time = Date.now() * 0.001;

    group.rotation.y = time * 0.1;
    renderer.render( scene, camera );

}

// Update the scene if the user resize the window
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
})
