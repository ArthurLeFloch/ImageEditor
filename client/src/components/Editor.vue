<script setup>
import {ref, onMounted} from "vue";
import {useRouter} from "vue-router";

import ImageViewer from "@/components/viewer/ImageViewer.vue";
import ActionButtons from "@/components/panel/ActionButtons.vue";
import SideButtons from "@/components/SideButtons.vue";
import CancelIcon from "@/icons/CancelIcon.vue";
import ContinueIcon from "@/icons/ContinueIcon.vue";

const router = useRouter();

onMounted(() => router.push('/'));

function selectRoute(route) {
  resetImage();
  if (route !== router.currentRoute.value.path) {
    router.push(route);
    return;
  }
  router.push('/');
}

// TODO: Once file imported, change route to the requested one instead of "/"
// /transform /?next=transform /transform

// FIXME: On firefox mobile, download image doesn't work when not in the "/" route
// FIXME: On firefox mobile, the image won't upload properly to the server (hangs on request.files)

const isModified = ref(false);

async function getMetadata(file) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      resolve({
        name: file.name ? file.name : savedImage.value.metadata.name,
        width: image.width,
        height: image.height
      });
    }
    image.onerror = reject;
    image.src = URL.createObjectURL(file);
  });
}

const savedImage = ref(null);
const shownImage = ref(null);

async function setImage(file) {
  isModified.value = false;
  const url = URL.createObjectURL(file);
  const metadata = await getMetadata(file);
  savedImage.value = {
    file, url, metadata
  };
  shownImage.value = {
    file, url, metadata
  };
}

async function setShownImage(file) {
  isModified.value = true;
  const url = URL.createObjectURL(file);
  const metadata = await getMetadata(file);
  shownImage.value = {
    file, url, metadata
  };
}

function acceptImage() {
  isModified.value = false;
  savedImage.value = shownImage.value;
}

function resetImage() {
  isModified.value = false;
  shownImage.value = savedImage.value;
}

function getSavedFile() {
  return savedImage.value.file;
}

function onImport(event) {
  setImage(event.target.files[0]);
}

function clickImport() {
  document.getElementById('import').click();
}

// Handle drag and drop
const isDropping = ref(false);

function setDropping(value) {
  isDropping.value = value;
}

function handleDrop(event) {
  setDropping(false);
  setImage(event.dataTransfer.files[0]);
}

function downloadImage() {
  const a = document.createElement('a');
  a.href = shownImage.value.url;
  let name = shownImage.value.metadata.name;
  if (name.includes('.'))
    name = name.substring(0, name.lastIndexOf('.'));
  a.download = `${name}_edited.png`;
  a.click();
}
</script>

<template>
  <main id="editor">
    <input type="file" id="import" @change="onImport" style="display: none"
           accept="image/bmp, image/jpeg, image/jpg, image/png"/>
    <ActionButtons :selectRoute="selectRoute" :active="!!shownImage && shownImage.file !== null"/>
    <Transition name="slide">
      <div id="editor__action_details" v-show="router.currentRoute.value.path !== '/'">
        <router-view :getFile="getSavedFile" :setFile="setShownImage" :resetFile="resetImage"/>
      </div>
    </Transition>
    <div id="editor__content"
         @drop.prevent="handleDrop"
         @dragenter.prevent="setDropping(true)"
         @dragleave.prevent="setDropping(false)"
         @dragover.prevent.stop>
      <ImageViewer :image="shownImage ? shownImage.url: null" @import="clickImport"
                   :metadata="shownImage ? shownImage.metadata : null">
        <template v-slot:cancel_button v-if="isModified">
          <button id="editor__cancel_button" title="Cancel" @click="resetImage">
            <CancelIcon/>
          </button>
        </template>
        <template v-slot:continue_button v-if="isModified">
          <button id="editor__continue_button" title="Continue" @click="acceptImage">
            <ContinueIcon/>
            <span>
            Continue
          </span>
          </button>
        </template>
      </ImageViewer>
      <SideButtons @import="clickImport" @download="downloadImage"
                   :hasImage="!!shownImage && shownImage.file !== null"/>
    </div>
  </main>
</template>

<style scoped>
#editor {
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  background-color: var(--primary-bg-3);
}

#editor__action_details {
  overflow-y: auto;
  background-color: var(--primary-bg-2);
  width: var(--editor-action-details-size);
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
  box-shadow: 0 0 8px 0 rgba(0, 0, 0, 0.5);
  flex-shrink: 0;
  z-index: 0;
  padding: 1rem;
}

#editor__action_details::v-deep(input) {
  padding: 0.5rem;
  border: 2px solid var(--primary-fg-3);
  border-radius: 0.5rem;
  background-color: var(--primary-bg-2);
  color: var(--primary-fg-1);
}

#editor__action_details::v-deep(select) {
  padding: 0.5rem;
  border: 2px solid var(--primary-fg-3);
  border-radius: 0.5rem;
  background-color: var(--primary-bg-2);
  color: var(--primary-fg-1);
  cursor: pointer;
}

.slide-leave-active, .slide-enter-active {
  transition: transform 0.3s ease;
}

.slide-enter-from, .slide-leave-to {
  transform: translateX(-100%);
}

#editor__content {
  flex-grow: 1;
  position: relative;
}

#editor__cancel_button, #editor__continue_button {
  border: none;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
}

#editor__continue_button {
  background-color: var(--correct-color);
  border: 2px solid var(--correct-color);
  align-self: flex-end;
  color: white;
  font-size: 1rem;
}

#editor__continue_button:hover {
  background-color: var(--correct-hover-color);
  border: 2px solid var(--correct-hover-color);
}

#editor__continue_button > span {
  margin-left: 0.5rem;
}

#editor__cancel_button {
  background-color: transparent;
  border: 2px solid var(--incorrect-color);
  align-self: center;
}

#editor__cancel_button > svg {
  width: 24px;
  height: 24px;
  fill: var(--incorrect-color);
}

#editor__cancel_button:hover {
  background-color: var(--incorrect-color);
}

#editor__cancel_button:hover > svg {
  fill: white;
}

#editor__continue_button > svg {
  width: 24px;
  height: 24px;
  fill: white;
}

@media screen and (max-width: 576px) {
  #editor {
    flex-direction: column-reverse;
  }

  #editor__action_details {
    height: var(--editor-action-details-size);
    width: 100%;
    overflow-x: scroll;
    border-radius: 0;
  }

  #editor__content {
    height: 0;
  }

  .slide-leave-active, .slide-enter-active {
    transition: transform 0.3s ease;
  }

  .slide-enter-from, .slide-leave-to {
    transform: translateY(100%);
  }

  #editor__continue_button > span {
    display: none;
  }
}
</style>