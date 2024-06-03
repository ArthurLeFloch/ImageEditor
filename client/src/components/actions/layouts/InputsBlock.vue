<script setup>
import {computed, useSlots} from "vue";
import ForwardIcon from "@/icons/ForwardIcon.vue";
import SubActionButton from "@/components/panel/SubActionButton.vue";

defineProps({
  isValid: {
    type: Boolean,
    default: true
  },
  onClick: Function
})

const slots = useSlots();
const inputCount = computed(() => {
  return slots.default ? slots.default().length : 0;
});

const gridStyle = computed(() => {
  return {
    display: 'grid',
    gridTemplateColumns: '1fr auto',
    gridTemplateRows: `repeat(${inputCount.value}, auto)`,
    gap: '0.5rem'
  }
});

const buttonStyle = computed(() => {
  return {
    gridColumn: '2',
    gridRow: `1 / span ${inputCount.value}`
  }
});
</script>

<template>
  <div :style="gridStyle" class="input_block">
    <slot></slot>
    <SubActionButton :action="onClick" :icon="ForwardIcon" :blocked="!isValid" :style="buttonStyle"/>
  </div>
</template>

<style scoped>
.input_block::v-deep(input) {
  grid-column: 1;
  width: 100%;
}
</style>