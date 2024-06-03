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

const grayFormula = ref('none');

const basicFilterKernel = ref('3');
const basicFilterType = ref('none');

const sobelKernel = ref('all');
const sobelThreshold = ref(0.5);

const gaussianSigmaX = ref(0.8);
const gaussianSigmaY = ref(0.8);
const gaussianKernelSize = ref('3');

const bilateralSigmaColor = ref(75);
const bilateralSigmaSpace = ref(75);
const bilateralKernel = ref('3');

async function grayscale() {
  await fetchImage('grayscale', {formula: grayFormula.value});
}

async function basicConvolution() {
  await fetchImage('convolution', {
    kernel_size: basicFilterKernel.value,
    kernel_type: basicFilterType.value
  });
}

async function sobel() {
  await fetchImage('sobel', {
    sobel_type: sobelKernel.value,
    threshold: sobelThreshold.value
  });
}

async function gaussian() {
  await fetchImage('convolution', {
    kernel_type: 'gaussian',
    kernel_size: gaussianKernelSize.value,
    sigma_x: gaussianSigmaX.value,
    sigma_y: gaussianSigmaY.value
  });
}

async function bilateral() {
  await fetchImage('bilateral', {
    kernel_size: bilateralKernel.value,
    sigma_color: bilateralSigmaColor.value,
    sigma_space: bilateralSigmaSpace.value
  });
}
</script>

<template>
  <TransformSection title="Grayscale">
    <InputsBlock :onClick="() => grayscale()" :isValid="grayFormula !== 'none'">
      <select v-model="grayFormula">
        <option selected value="none" disabled>Formula...</option>
        <option value="luminosity">Luminosity</option>
        <option value="average">Average</option>
      </select>
    </InputsBlock>
  </TransformSection>

  <TransformSection title="Basic filters">
    <InputsBlock :onClick="() => basicConvolution()"
                 :isValid="basicFilterKernel !== 'none' && basicFilterType !== 'none'">
      <select v-model="basicFilterKernel" title="Kernel size">
        <option selected value="3">3 x 3</option>
        <option value="5">5 x 5</option>
        <option value="7">7 x 7</option>
      </select>
      <select v-model="basicFilterType" title="Convolution type">
        <option selected disabled value="none">Type...</option>
        <option value="average">Average</option>
        <option value="median">Median</option>
      </select>
    </InputsBlock>
  </TransformSection>

  <TransformSection title="Gaussian blur">
    <InputsBlock :onClick="() => gaussian()"
                 :isValid="!!gaussianSigmaX && !!gaussianSigmaY && gaussianKernelSize !== 'none'">
      <select v-model="gaussianKernelSize" title="Kernel size">
        <option selected value="3">3 x 3</option>
        <option value="5">5 x 5</option>
        <option value="7">7 x 7</option>
      </select>
      <input type="number" v-model="gaussianSigmaX" min="0" step="0.1" placeholder="Sigma X" title="Sigma X"/>
      <input type="number" v-model="gaussianSigmaY" min="0" step="0.1" placeholder="Sigma Y" title="Sigma Y"/>
    </InputsBlock>
  </TransformSection>

  <TransformSection title="Sobel">
    <InputsBlock :onClick="() => sobel()" :isValid="sobelKernel !== 'none'">
      <select v-model="sobelKernel" title="Sobel kernel">
        <option selected value="all">Full Sobel</option>
        <option value="x">Sobel X</option>
        <option value="y">Sobel Y</option>
      </select>
      <input type="number" v-model="sobelThreshold" min="0" step="0.01" max="1" placeholder="Threshold"
             :title="'Threshold'"/>
    </InputsBlock>
  </TransformSection>

  <TransformSection title="Bilateral filter">
    <InputsBlock :onClick="() => bilateral()" :isValid="sobelKernel !== 'none'">
      <select v-model="bilateralKernel" title="Kernel size">
        <option selected value="3">3 x 3</option>
        <option value="5">5 x 5</option>
        <option value="7">7 x 7</option>
        <option value="9">9 x 9</option>
      </select>
      <input type="number" v-model="bilateralSigmaColor" min="0" step="0.1" placeholder="Color Sigma"
             title="Color Sigma">
      <input type="number" v-model="bilateralSigmaSpace" min="0" step="0.1" placeholder="Space Sigma"
             title="Space Sigma">
    </InputsBlock>
  </TransformSection>
</template>

<style scoped>
</style>