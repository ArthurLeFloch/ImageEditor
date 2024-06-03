<script setup>
import {ref} from 'vue';

// metadata not null from ImageViewer.vue

defineProps({
  metadata: {
    type: Object,
    required: true
  }
});

</script>

<template>
  <div id="metadata">
    <p id="metadata__name">
      {{ metadata.name }}
    </p>
    <p id="metadata__size">
      {{ metadata.width }}x{{ metadata.height }}
    </p>
  </div>
</template>

<style scoped>
#metadata {
  text-align: center;
  overflow: hidden;
  width: 0;
  flex-grow: 1;
}

#metadata__name {
  font-weight: bold;
  color: var(--primary-fg-1);
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

#metadata__size {
  color: var(--primary-fg-2);
  white-space: nowrap;
  overflow: hidden;
}

</style>