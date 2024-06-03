<script setup>
import DownloadIcon from "@/icons/DownloadIcon.vue";
import UploadIcon from "@/icons/UploadIcon.vue";

defineProps({
  hasImage: Boolean
})

const emit = defineEmits(['import', 'download']);

</script>

<template>
  <div id="viewer__side_buttons">
    <button id="viewer__side_button" title="Import image" @click="$emit('import')">
      <UploadIcon/>
    </button>
    <button id="viewer__side_button" title="Download image" @click="$emit('download')" :class="{disabled: !hasImage}">
      <DownloadIcon/>
    </button>
  </div>
</template>

<style scoped>
#viewer__side_buttons {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  position: absolute;
  top: 0;
  right: 0;
  padding: 0.5rem;
}

#viewer__side_button {
  border: 2px solid var(--primary-fg-3);
  background-color: var(--primary-bg-3);
  border-radius: 8px;
  padding: 0.25rem;
  margin: 0.5rem;
  cursor: pointer;
}

#viewer__side_button:hover {
  background: var(--primary-bg-2);
}

#viewer__side_button > svg {
  fill: var(--primary-fg-2);
  width: 32px;
  height: 32px;
  display: block;
}

#viewer__side_button.disabled {
  background-color: var(--primary-bg-1);
  cursor: not-allowed;
  pointer-events: none;
}
</style>