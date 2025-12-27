<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <section class="layout-card">
    <header class="layout-card__header">
      <slot name="header">
        <h2 class="layout-card__title">{{ title }}</h2>
      </slot>
    </header>

    <div class="layout-card__body">
      <slot />
    </div>

    <footer class="layout-card__footer">
      <slot name="footer" />
    </footer>
  </section>
</template>

<style scoped>
.layout-card {
  border: 1px solid rgba(128, 128, 128, 0.25);
  border-radius: 14px;
  padding: 16px;
}
.layout-card__header {
  margin-bottom: 12px;
}
.layout-card__title {
  margin: 0;
}
.layout-card__footer {
  margin-top: 12px;
}
</style>
