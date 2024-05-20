import React from "react";
import { useCamera } from "../../useContext/CameraContext";

export function TopSection() {
    const { moveCamera } = useCamera();

    const handleClick1 = () => {
        // Example: move the camera to a new position
        moveCamera([0, 1, 5]);
    };
    const handleClick2 = () => {
        // Example: move the camera to a new position
        moveCamera([0, 0, 18]);
    };
    const handleClick3 = () => {
        // Example: move the camera to a new position
        moveCamera([-2, 0, 5]);
    };

    return (
        <div className="absolute w-full h-full z-50">
            <div className="hero min-h-screen">
                <div className="hero-content text-center bg-opacity-30 backdrop-blur-sm rounded-lg bg-gray-600 p-10">
                    <div className="">
                        <h1 className="text-5xl font-bold">Hello there</h1>
                        <p className="py-6">
                            Provident cupiditate voluptatem et in. Quaerat
                            fugiat ut assumenda excepturi exercitationem quasi.
                            In deleniti eaque aut repudiandae et a id nisi.
                        </p>
                        <div className="flex gap-4 flex-col my-4">
                            <div className="overflow-x-auto">
                                <table className="table">
                                    {/* head */}
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Type</th>
                                            <th>Status</th>
                                            <th>Capacity</th>
                                            <th></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {/* row 1 */}
                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>
                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>
                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>
                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>
                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>
                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>
                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>

                                        <tr>
                                            <td>
                                                <div className="flex items-center gap-3">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img
                                                                src="https://www.cnet.com/a/img/resize/1a01b6b074937ad937e9eb4430bd21fa5bf31957/hub/2019/01/11/21c3dece-7bbb-4fba-8fca-10c894b8b39a/starship.jpg?auto=webp&width=1200"
                                                                alt="Avatar Tailwind CSS Component"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="font-bold">
                                                        Starship
                                                        </div>
                                                        <div className="text-sm opacity-50">Space-X
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                Launch Rocket
                                            </td>
                                            <td>
                                                Needs Repair
                                            </td>
                                            <td>350kg</td>
                                            <th>
                                                <button className="btn btn-ghost btn-xs">
                                                    details
                                                </button>
                                            </th>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div className="flex gap-5 justify-center">
                            <button
                                onClick={handleClick1}
                                className="btn btn-primary"
                            >
                                1. pozisyon
                            </button>
                            <button
                                onClick={handleClick2}
                                className="btn btn-primary"
                            >
                                2. pozisyon
                            </button>
                            <button
                                onClick={handleClick3}
                                className="btn btn-primary"
                            >
                                3. pozisyon
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
