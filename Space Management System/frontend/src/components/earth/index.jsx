"use client";

import React, { useRef } from "react";
import { useFrame, useLoader } from "@react-three/fiber";
import { PerspectiveCamera, OrbitControls, Stars } from "@react-three/drei";
import * as THREE from "three";
import { TextureLoader } from "three";
import { useCamera } from "../../useContext/CameraContext";
import { useSpring, a } from "@react-spring/three";
import { useThree } from "@react-three/fiber";
import { useEffect } from "react";

const CameraAnimator = ({ position }) => {
    const { camera } = useThree();
    const props = useSpring({
        to: { position: position },
        config: { mass: 5, tension: 10, friction: 16 },
    });
    return <a.primitive object={camera} {...props} />;
};


function ParallaxEffect() {
    const { camera } = useThree();
    useEffect(() => {
        const handleMouseMove = (event) => {
            const { innerWidth, innerHeight } = window;
            const mouseX = (event.clientX / innerWidth) * 2 - 1;
            const mouseY = -(event.clientY / innerHeight) * 2 + 1;

            const finalX = mouseX * 0.5;
            const finalY = mouseY * 0.5;

            camera.position.x += (finalX - camera.position.x) * 0.05;
            camera.position.y += (finalY - camera.position.y) * 0.05;
            camera.lookAt(0, 0, 0);
        };

        window.addEventListener("mousemove", handleMouseMove);

        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
        };
    }, [camera]);

    return null;
}

export function Earth(props) {
    const EarthDayMap = "/assets/textures/Earth_Diffuse_6K.jpg";
    const EarthNormalMap = "/assets/textures/Earth_NormalNRM_6K.jpg";
    const EarthSpecularMap = "/assets/textures/Earth_Glossiness_6K.jpg";
    const EarthCloudsMap = "/assets/textures/Earth_Clouds_6K.jpg";
    const [colorMap, normalMap, specularMap, cloudsMap] = useLoader(
        TextureLoader,
        [EarthDayMap, EarthNormalMap, EarthSpecularMap, EarthCloudsMap]
    );

    const { position } = useCamera();

    const earthRef = useRef();
    const cloudsRef = useRef();

    useFrame(({ clock }) => {
        const elapsedTime = clock.getElapsedTime();

        earthRef.current.rotation.y = elapsedTime / 26;
        cloudsRef.current.rotation.y = elapsedTime / 24;
    });

    return (
        <>
            <CameraAnimator position={position}/>
            <PerspectiveCamera makeDefault position={[0, 0, 18]} fov={30}/>
            <ambientLight intensity={0.8} />
            <pointLight
                castShadow="true"
                color="#fbfdff"
                position={[-4, 3, 4]}
                intensity={645}
            />
            <Stars
                radius={300}
                depth={60}
                count={40000}
                factor={7}
                saturation={0}
                fade={true}
            />
            <mesh ref={cloudsRef} position={[0, -1, 0]}>
                <sphereGeometry args={[2.02, 32, 32]} />
                <meshPhongMaterial
                    map={cloudsMap}
                    opacity={0.4}
                    depthWrite={true}
                    transparent={true}
                    side={THREE.DoubleSide}
                />
            </mesh>
            <mesh ref={earthRef} position={[0, -1, 0]}>
                <sphereGeometry args={[2, 64, 32]} />
                <meshPhongMaterial specularMap={specularMap} />
                <meshStandardMaterial
                    map={colorMap}
                    normalMap={normalMap}
                    metalness={0.4}
                    roughness={0.7}
                />
            </mesh>
        </>
    );
}
