<script setup>
defineProps({
    show: Boolean
})

defineEmits(['close'])
</script>

<template>
    <div v-if="show" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click="$emit('close')">
        <div class="bg-white rounded-xl shadow-lg max-w-xl w-full p-6 relative" @click.stop>

            <h1 class="text-3xl font-bold text-black text-center">
                Help
            </h1>

            <p class="mt-4 text-gray-500 text-center">
                Learn how to use the Cambodian Sign Language Recognition system
            </p>

            <div class="mt-10 space-y-6">
                <div class="p-6 border border-gray-200 rounded-xl shadow-sm">
                    <h2 class="text-lg font-semibold text-black">
                        1. Use Webcam
                    </h2>
                    <p class="mt-2 text-gray-500">
                        Click Use Webcam to recognize sign language in real time using your camera.
                    </p>
                </div>
                <div class="p-6 border border-blue-100 bg-blue-50 rounded-xl">
                    <h2 class="text-lg font-semibold text-blue-900">
                        Tips for Better Recognition
                    </h2>
                    <ul class="mt-3 text-gray-600 list-disc list-inside space-y-1">
                        <li>Use good lighting.</li>
                        <li>Keep your hands clearly inside the camera frame.</li>
                        <li>Avoid dark backgrounds.</li>
                        <li>Make the sign clearly and slowly.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>