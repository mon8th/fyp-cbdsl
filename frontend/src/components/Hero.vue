<script setup>
import { ref } from 'vue'
import Webcam from './Webcam.vue'
import CamIcon from '../assets/CamIcon.vue'
import DropdownIcon from '../assets/DropdownIcon.vue'

const selectedModel = ref('Choose a model')
const showWebcam = ref(false)

const handleModelSelect = (model) => {
    selectedModel.value = model
}

const useWebCam = () => {
    if (selectedModel.value === 'Choose a model') {
        alert('Please choose a model')
        return
    }
    showWebcam.value = true
}
</script>

<template>
    <div class="flex flex-col items-center justify-center py-10">
        <h1 class="text-3xl font-semibold text-black">Cambodian Sign Language Recognition</h1>
        <p class="mt-5 text-gray-500 text-center">Choose an option below to get started</p>
        <el-dropdown trigger="click" @command="handleModelSelect" class="mt-6">
            <button type="button"
                class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition">
                {{ selectedModel }}
                <DropdownIcon />
            </button>

            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item command="ResNet50">ResNet50</el-dropdown-item>
                    <el-dropdown-item command="YOLOv8">YOLOv8</el-dropdown-item>
                    <el-dropdown-item command="MediaPipe + MLP">MediaPipe + MLP</el-dropdown-item>
                    <el-dropdown-item command="EfficientNetB0">EfficientNetB0</el-dropdown-item>
                    <el-dropdown-item command="MobileNetV2">MobileNetV2</el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </div>
    <div v-if="!showWebcam" class="flex justify-center gap-12">
        <div class="w-80 p-6 border border-gray-200 rounded-xl shadow-sm">
            <CamIcon class="w-16 h-16 mx-auto rounded-full bg-blue-200 p-3" />
            <h2 class="mt-4 text-lg font-semibold text-center">
                Use Webcam
            </h2>
            <p class="mt-2 text-sm text-gray-500 text-center">
                Use your webcam for real-time sign language recognition
            </p>
            <button @click="useWebCam"
                class="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 cursor-pointer transition">
                Use Webcam
            </button>
            <p class="mt-2 text-xs text-gray-400 text-center">
            </p>
        </div>
    </div>
    <Webcam
        v-if="showWebcam"
        :model="selectedModel"
        @close="showWebcam = false"
    />
</template>