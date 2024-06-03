<script setup>
import FilterIcon from "@/icons/FilterIcon.vue";
import TransformIcon from "@/icons/TransformIcon.vue";
import ExperimentIcon from "@/icons/ExperimentIcon.vue";

const props = defineProps({
  selectRoute: {
    type: Function,
    required: true
  },
  active: {
    type: Boolean,
    required: true
  }
});

</script>

<template>
  <!-- If current route is /, then block the buttons -->
  <div id="actions" :class="{ 'inactive': !props.active }">
    <router-link class="action__button" @click="props.selectRoute('/transform')" to="/transform">
      <TransformIcon/>
      Adjust
    </router-link>
    <router-link class="action__button" @click="props.selectRoute('/filter')" to="/filter">
      <FilterIcon/>
      Filter
    </router-link>
    <router-link class="action__button" @click="props.selectRoute('/experiment')" to="/experiment">
      <ExperimentIcon/>
      Special
    </router-link>
  </div>
</template>

<style scoped>
#actions {
  background-color: var(--primary-bg-1);
  width: var(--editor-action-size);
  display: flex;
  align-items: center;
  flex-direction: column;
  z-index: 1;
  flex-shrink: 0;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-gutter: initial;
}

#actions.inactive {
  cursor: not-allowed;
}

#actions.inactive > a {
  pointer-events: none;
  opacity: 0.4;
}

.action__button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: none;
  padding: 0.3rem 0;
  margin-bottom: 1rem;
  width: 100%;
  color: var(--primary-fg-1);
  font-size: 0.85rem;
  text-decoration: none;
}

.action__button:last-child {
  margin-bottom: 0;
}

.action__button:hover:not(.router-link-active) {
  border-radius: 16px;
  background-color: var(--primary-bg-2);
  cursor: pointer;
}

.action__button > svg {
  width: 32px;
  height: 32px;
  margin-bottom: 0.5rem;
  fill: var(--primary-fg-1);
}

.router-link-active {
  background-color: var(--primary-bg-2);
  font-weight: bold;
}

@media screen and (max-width: 576px) {
  #actions {
    width: 100%;
    flex-direction: row;
    display: flex;
    justify-content: flex-start;
    gap: 0.5em;
    overflow-x: auto;
    padding: 0 0.5em;
  }

  .action__button {
    margin-bottom: 0;
    min-width: 64px;
    padding: 0.5em 0.5em 0.8em;
  }
}
</style>