<script setup>
import SignIcon from '../../assets/SignIcon.vue'
import QuestionIcon from '../../assets/QuestionIcon.vue'
</script>

<template>
    <nav class="w-full bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="w-10 flex items-center justify-center">
                <SignIcon />
            </div>
            <h1 class="text-xl font-bold text-black">
                CBDSL <span class="text-blue-900">Recognition</span>
            </h1>
        </div>

        <div class="flex items-center gap-2 text-black-300 text-sm">
            <div >
                <QuestionIcon />
            </div>
            <a href="#" class="hover:text-blue-900">Help</a>
        </div>
    </nav>
</template>