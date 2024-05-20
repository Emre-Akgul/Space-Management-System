
"use client";
import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import dynamic from 'next/dynamic';
import { Earth } from "../components/earth";
import { CameraProvider } from "../useContext/CameraContext";
import { TopSection } from "../components/topSection";

function App() {
  return (
    <CameraProvider>
      <div className=" w-full h-full">
        <TopSection />
        <Canvas className=" w-full h-full">
          <Suspense fallback={null}>
            <Earth />
          </Suspense>
        </Canvas>
      </div>
    </CameraProvider>
  );
}

export default App;