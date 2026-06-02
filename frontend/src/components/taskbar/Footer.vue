<script setup>
import niseLogo from '../../assets/NISE.png'
import paragonLogo from '../../assets/Paragon.svg'
</script>

<template>
    <footer class="mt-25 border-t border-gray-200 py-4">
        <div class="text-center">
            <p class="text-sm text-gray-500">
                Developed as part of the Cambodian Sign Language Recognition Project
            </p>

            <div class="flex items-center justify-center gap-3 mt-2">
                <span class="text-sm text-gray-500">Supported by</span>
                <img :src="niseLogo" alt="NISE" class="h-10 object-contain" />
                <span class="text-gray-300">|</span>
                <img :src="paragonLogo" alt="Paragon" class="h-8 object-contain" />
            </div>
        </div>
    </footer>
</template>