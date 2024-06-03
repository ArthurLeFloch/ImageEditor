<script setup>
import ImageMetadata from "@/components/viewer/ImageMetadata.vue";

const props = defineProps({
  image: {
    type: String,
    default: null
  },
  metadata: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['import']);
</script>

<template>
  <div id="viewer">
    <img v-if="image" id="image" v-bind:src="props.image" alt="Image"/>
    <div v-else id="viewer__ask_import">
      <p>
        Drop an image here, or
        <button id="viewer__first_import" @click="$emit('import')">click here</button>
        to import one...
      </p>
    </div>

    <div id="viewer__bottom">
      <slot name="cancel_button"/>
      <ImageMetadata v-if="props.metadata" :metadata="props.metadata"/>
      <slot name="continue_button"/>
    </div>
  </div>
</template>

<style scoped>

#viewer {
  display: flex;
  justify-content: center;
  height: 100%;
  flex-direction: column;
}

#viewer > img {
  flex-grow: 1;
  padding: 1rem;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  image-rendering: pixelated;
  height: 0;
}

#viewer__ask_import {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-grow: 1;
  padding: 1.5rem;
}

#viewer__ask_import > p {
  font-size: 1.25rem;
  color: var(--primary-fg-1);
}

#viewer__first_import {
  display: inline;
  background-color: transparent;
  border: none;
  color: var(--primary-fg-1);
  cursor: pointer;
  font-weight: bold;
  font-size: 1.25rem;
}

#viewer__first_import:hover {
  text-decoration: underline;
  text-underline-position: under;
}

#viewer__bottom {
  gap: 1rem;
  display: flex;
  justify-content: space-between;
  padding: 0.5em 1em;
}

</style>