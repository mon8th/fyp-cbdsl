<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
    model: {
        type: String,
        required: true
    }
})

const emit = defineEmits(['close'])

const videoRef = ref(null)
const canvasRef = ref(null)
const prediction = ref('—')
const errorMessage = ref('')
const isProcessing = ref(false)

let intervalId = null

const startCamera = async () => {
    try {
        const canvas = canvasRef.value
        canvas.width = 224
        canvas.height = 224

        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        })

        videoRef.value.addEventListener(
            'loadedmetadata',
            () => {
                intervalId = setInterval(sendFrame, 300)
            },
            { once: true }
        )

        videoRef.value.srcObject = stream

    } catch (error) {
        console.error(error)
        errorMessage.value = 'Unable to access webcam.'
    }
}

const stopCamera = () => {
    clearInterval(intervalId)

    const stream = videoRef.value?.srcObject

    if (stream) {
        stream.getTracks().forEach(track => track.stop())
    }

    emit('close')
}

const sendFrame = async () => {
    if (isProcessing.value) return

    const video = videoRef.value
    const canvas = canvasRef.value

    if (!video || !canvas) return

    if (!props.model) {
        errorMessage.value = 'No model selected.'
        return
    }

    isProcessing.value = true

    const ctx = canvas.getContext('2d')

    ctx.save()
    ctx.scale(-1, 1)

    ctx.drawImage(
        video,
        -canvas.width,
        0,
        canvas.width,
        canvas.height
    )

    ctx.restore()

    canvas.toBlob(async (blob) => {
        if (!blob) {
            isProcessing.value = false
            errorMessage.value = 'Failed to capture webcam frame.'
            return
        }

        const formData = new FormData()
        formData.append('image', blob, 'frame.jpg')
        formData.append('model', props.model)

        try {
            const res = await fetch('http://localhost:8000/predict/webcam', {
                method: 'POST',
                body: formData
            })

            const data = await res.json()

            prediction.value = data.prediction ?? '—'

        } catch (error) {
            console.error(error)
            errorMessage.value = 'Cannot connect to prediction server.'
        } finally {
            isProcessing.value = false
        }
    }, 'image/jpeg')
}

onMounted(() => {
    startCamera()
})

onUnmounted(() => {
    clearInterval(intervalId)

    const stream = videoRef.value?.srcObject

    if (stream) {
        stream.getTracks().forEach(track => track.stop())
    }
})
</script>

<template>
    <div class="mt-10 flex flex-col items-center">
        <video ref="videoRef" autoplay playsinline
            class="w-full max-w-2xl rounded-xl border border-gray-200 shadow-sm scale-x-[-1]"></video>

        <canvas ref="canvasRef" class="hidden"></canvas>

        <button class="mt-4 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600" @click="stopCamera">
            Stop Webcam
        </button>

        <div class="mt-6 text-center">
            <p class="text-sm text-gray-500">Model</p>
            <p class="font-semibold">{{ model }}</p>

            <p class="mt-4 text-sm text-gray-500">Prediction</p>
            <p class="text-xl font-semibold">{{ prediction }}</p>
        </div>
    </div>
</template>