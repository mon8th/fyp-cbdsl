<script setup>
import { ref } from 'vue'
import SignIcon from '../../assets/SignIcon.vue'
import QuestionIcon from '../../assets/QuestionIcon.vue'
import Help from '../Help.vue'

const showHelp = ref(false)
</script>

<template>
    <nav class="sticky top-0 z-50 w-full bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="w-10 flex items-center justify-center">
                <SignIcon />
            </div>

            <h1 class="text-xl font-bold text-black">
                CBDSL <span class="text-blue-900">Recognition</span>
            </h1>
        </div>

        <button @click="showHelp = true" class="flex items-center gap-2 text-sm text-gray-500 cursor-pointer hover:text-blue-900">
            <QuestionIcon />
            Help
        </button>

        <Help :show="showHelp" @close="showHelp = false" />
    </nav>
</template>