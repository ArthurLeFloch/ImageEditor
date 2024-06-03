<script setup>

const props = defineProps({
  text: String,
  action: Function,
  icon: Object,
  blocked: {
    type: Boolean,
    default: false
  },
});
</script>

<template>
  <button @click="action" :class="['sub_action_button', blocked ? 'blocked' : '']">
    <component :is="icon"/>
    <span v-if="text">{{ text }}</span>
  </button>
</template>

<style scoped>
.sub_action_button {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-bg-2);
  color: var(--primary-fg-1);
  border: 2px solid var(--primary-fg-3);
  border-radius: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
}

.sub_action_button.blocked {
  background-color: var(--primary-bg-1);
  pointer-events: none;
}

.sub_action_button::v-deep(svg) {
  width: 1.5rem;
  height: 1.5rem;
  fill: var(--primary-fg-1);
}

.sub_action_button:hover {
  background-color: var(--primary-bg-1);
}


</style>