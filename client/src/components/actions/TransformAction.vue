<script setup>

import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';
import {onUnmounted, ref} from "vue";
import SubActionButton from "@/components/panel/SubActionButton.vue";
import RotateRightIcon from "@/icons/RotateRightIcon.vue";
import RotateLeftIcon from "@/icons/RotateLeftIcon.vue";
import CropIcon from "@/icons/CropIcon.vue";
import FlipVertical from "@/icons/FlipVerticalIcon.vue";
import FlipHorizontal from "@/icons/FlipHorizontalIcon.vue";
import InputsBlock from "@/components/actions/layouts/InputsBlock.vue";
import ButtonsBlock from "@/components/actions/layouts/ButtonsBlock.vue";
import TransformSection from "@/components/actions/layouts/TransformSection.vue";
import CancelIcon from "@/icons/CancelIcon.vue";
import {useActionDetailsProps} from "@/components/panel/utils.js";

const props = defineProps({
  getFile: Function,
  setFile: Function,
  resetFile: Function,
});
const fetchImage = useActionDetailsProps(props);

const padding = ref('none');

const cropper = ref(null);

function startCrop() {
  props.resetFile();
  const image = document.getElementById('image');
  cropper.value = new Cropper(image, {
    viewMode: 1,
  });
}

async function applyCrop() {
  if (!cropper.value) {
    console.error('Cropper is not initialized');
    return;
  }
  const file = await fetch(cropper.value.getCroppedCanvas().toDataURL())
      .then(response => response.blob());
  props.setFile(file);

  cropper.value.destroy();
  cropper.value = null;
}

function stopCrop() {
  if (cropper.value) {
    cropper.value.destroy();
    cropper.value = null;
  }
}

onUnmounted(() => {
  if (cropper.value) {
    cropper.value.destroy();
    cropper.value = null;
  }
});

const rotation = ref(null);

async function rotate(angle) {
  if (angle % 90 === 0) {
    await fetchImage('rotate', {angle, padding: 'transparent'});
    return;
  }
  await fetchImage('rotate', {angle, padding: padding.value});
}

const width = ref(null);
const height = ref(null);

async function resize(width, height) {
  await fetchImage('resize', {width, height});
}

async function flip(axis) {
  await fetchImage('flip', {axis});
}
</script>

<template>
  <TransformSection title="Rotation">
    <ButtonsBlock>
      <SubActionButton :text="'-90°'" :action="() => rotate(-90)" :icon="RotateLeftIcon"/>
      <SubActionButton :text="'+90°'" :action="() => rotate(90)" :icon="RotateRightIcon"/>
    </ButtonsBlock>
    <InputsBlock :onClick="() => rotate(rotation)" :isValid="!!rotation && padding !== 'none'">
      <input type="number" id="rotation" v-model="rotation" min="-360" max="360" step="15" placeholder="Angle"/>
      <select v-model="padding" title="Padding">
        <option selected disabled value="none">Padding...</option>
        <option value="transparent">Transparent</option>
        <option value="black">Black</option>
        <option value="white">White</option>
        <option value="no_resize">No resize</option>
      </select>
    </InputsBlock>
  </TransformSection>

  <TransformSection title="Flip">
    <ButtonsBlock>
      <SubActionButton :action="() => flip('vertical')" :icon="FlipVertical"/>
      <SubActionButton :action="() => flip('horizontal')" :icon="FlipHorizontal"/>
    </ButtonsBlock>
  </TransformSection>

  <TransformSection title="Crop">
    <ButtonsBlock>
      <SubActionButton :text="cropper ? 'Crop' : 'Start'"
                       :action="cropper ? applyCrop : startCrop"
                       :icon="CropIcon"/>
      <SubActionButton :text="'Stop'" :action="stopCrop" :icon="CancelIcon" :blocked="!cropper"/>
    </ButtonsBlock>

  </TransformSection>

  <TransformSection title="Resize">
    <InputsBlock :onClick="() => resize(width, height)" :isValid="width > 0 && height > 0">
      <input type="number" title="Width" id="width" placeholder="Width" v-model="width" min="1"/>
      <input type="number" title="Height" id="height" placeholder="Height" v-model="height" min="1"/>
    </InputsBlock>
  </TransformSection>
</template>

<style scoped>
</style>