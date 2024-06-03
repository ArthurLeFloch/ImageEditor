<script setup>
import InfoButton from "@/components/actions/layouts/InfoButton.vue";

defineProps({
  title: String,
  info: {
    type: String,
    default: ''
  }
});
</script>

<template>
  <div class="transform__section">
    <div class="transform__section_top">
      <p class="transform__section_title">
        {{ title }}
      </p>
      <InfoButton class="transform__section_info" v-if="info" :text="info"/>
    </div>

    <div class="transform__section_content">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.transform__section {
  margin-bottom: 3rem;
  font-size: 0.85rem;
}

.transform__section_top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.transform__section_top > svg {
  width: 1.25rem;
  height: 1.25rem;
  fill: var(--primary-fg-2);
}

.transform__section_title {
  font-weight: bold;
  color: var(--primary-fg-1);
}
</style>