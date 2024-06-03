<script setup>

</script>

<template>
  <div class="button_block">
    <slot></slot>
  </div>
</template>

<style scoped>
.button_block {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.button_block > * {
  width: 0;
  flex-grow: 1;
}
</style>