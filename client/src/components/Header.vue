<script setup>
import {ref} from "vue";

import LightModeIcon from "@/icons/LightModeIcon.vue";
import DarkModeIcon from "@/icons/DarkModeIcon.vue";
import AppIcon from "@/icons/AppIcon.vue";
import GithubIcon from "@/icons/GithubIcon.vue";

const theme = ref('light');

// Check user's color preferences
if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
  theme.value = 'dark';
  document.body.className = 'dark';
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
  theme.value = event.matches ? "dark" : "light";
  document.body.className = theme.value;
});

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  document.body.className = theme.value;
}

document.body.className = theme.value;
</script>

<template>
  <header id="header">
    <div id="header__title">
      <AppIcon/>
      <h1>Image Editor</h1>
    </div>
    <nav id="header__navbar">
      <button class="header__navbar_item" @click="toggleTheme">
        <LightModeIcon v-if="theme === 'dark'"/>
        <DarkModeIcon v-else/>
      </button>
      <a class="header__navbar_item" title="GitHub repository" href="https://github.com/ArthurLeFloch/ImageEditor">
        <GithubIcon/>
      </a>
    </nav>
  </header>
</template>

<style scoped>
#header {
  display: flex;
  align-items: center;
  background-color: var(--primary-bg-1);
}

#header__title {
  margin: 0.5rem auto 0.5rem 0.5rem;
  display: flex;
  align-items: center;
  font-size: 0.7rem;
  color: var(--primary-fg-1);
}

#header__title > svg {
  width: 2rem;
  height: 2rem;
  margin-right: 1rem;
}

#header__navbar {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

#header__navbar > * {
  margin: 0 0.5rem;
}

.header__navbar_item {
  background-color: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0.5rem;
  border: none;
}

.header__navbar_item:hover {
  background-color: var(--primary-bg-2);
  border-radius: 50%;
}

.header__navbar_item > svg {
  width: 1.5rem;
  height: 1.5rem;
  fill: var(--primary-fg-1);
}

</style>
