<script setup>
import UploadIcon from '../assets/UploadIcon.vue'
import CamIcon from '../assets/CamIcon.vue';
</script>

<template id="Hero">
    <div class="flex flex-col items-center justify-center py-15">
        <h1 class="text-3xl font-semibold text-black">Cambodian Sign Language Recognition</h1>
        <p class="mt-5 text-gray-500 text-center">Choose an option below to get started</p>
    </div>
    <div class="flex justify-center gap-12">
        <div class="w-80 p-6 border border-gray-200 rounded-xl shadow-sm">
            <UploadIcon class="w-16 h-16 mx-auto rounded-full bg-blue-200 p-3" />
            <h2 class="mt-4 text-lg font-semibold text-center">
                Upload Video
            </h2>
            <p class="mt-2 text-sm text-gray-500 text-center">
                Upload a video file and we'll recognize the sign language
            </p>
            <button class="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 cursor-pointer transition">
                Upload Video
            </button>
            <p class="mt-2 text-xs text-gray-400 text-center">
                Max file size: MB
            </p>
        </div>
        <div class="w-80 p-6 border border-gray-200 rounded-xl shadow-sm">
            <CamIcon class="w-16 h-16 mx-auto rounded-full bg-blue-200 p-3" />
            <h2 class="mt-4 text-lg font-semibold text-center">
                Use Webcam
            </h2>
            <p class="mt-2 text-sm text-gray-500 text-center">
                Use your webcam for real-time sign language recognition
            </p>
            <button class="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 cursor-pointer transition">
                Use Webcam
            </button>
            <p class="mt-2 text-xs text-gray-400 text-center">
            </p>
        </div>
    </div>
</template>