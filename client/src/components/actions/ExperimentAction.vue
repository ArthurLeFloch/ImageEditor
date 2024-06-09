<script setup>
import {ref} from "vue";

import TransformSection from "@/components/actions/layouts/TransformSection.vue";
import InputsBlock from "@/components/actions/layouts/InputsBlock.vue";
import {useActionDetailsProps} from "@/components/panel/utils.js";


const props = defineProps({
  getFile: Function,
  setFile: Function,
  resetFile: Function,
});
const fetchImage = useActionDetailsProps(props);

const colorSpace = ref('none');
const legofyWidth = ref(null);
const legofyHeight = ref(null);

function legofy() {
  fetchImage('legofy', {
    color_space: colorSpace.value,
    width: legofyWidth.value,
    height: legofyHeight.value
  });
}

const colorCalculation = ref('none');
const sectionCount = ref(null);

function segment() {
  fetchImage('segment', {
    color: colorCalculation.value,
    n: sectionCount.value
  });
}
</script>

<template>
  <TransformSection title="Legofy" info="Convert your image to a lego-colored image">
    <InputsBlock :onClick="() => legofy()" :isValid="colorSpace !== 'none' && !!legofyWidth && !!legofyHeight">
      <select v-model="colorSpace">
        <option selected disabled value="none">Color space...</option>
        <option value="rgb">RGB</option>
        <option value="luv">LUV</option>
        <option value="lab">LAB</option>
      </select>
      <input type="number" placeholder="Width" v-model="legofyWidth" min="0"/>
      <input type="number" placeholder="Height" v-model="legofyHeight" min="0"/>
    </InputsBlock>
  </TransformSection>

  <TransformSection title="Segment" info="Segment your image into regions of the same color">
    <InputsBlock :onClick="() => segment()" :isValid="colorCalculation !== 'none' && !!sectionCount">
      <select v-model="colorCalculation">
        <option selected disabled value="none">Calculation...</option>
        <option value="average">Average</option>
        <option value="center">Center</option>
      </select>
      <input type="number" placeholder="Sections" v-model="sectionCount" min="0"/>
    </InputsBlock>

  </TransformSection>
</template>

<style scoped>
</style>