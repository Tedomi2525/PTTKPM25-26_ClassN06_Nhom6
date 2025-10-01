<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-lg rounded-lg">
      <div class="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
        <h2 class="text-xl font-bold">{{ title }}</h2>
        <slot name="actions"></slot>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
<thead class="bg-blue-100 text-center">
  <tr>
    <th
      v-for="(col, index) in columns"
      :key="index"
      class="px-2 py-2 whitespace-nowrap"
    >
      {{ col.label }}
    </th>
    <th v-if="hasActions" class="px-2 py-2 whitespace-nowrap">Hành động</th>
  </tr>
</thead>
<tbody>
  <tr v-for="row in data" :key="row[idKey]" class="text-center border-b">
    <td
      v-for="(col, index) in columns"
      :key="index"
      class="px-2 py-1 whitespace-nowrap"
    >
      {{ row[col.field] }}
    </td>
    <td v-if="hasActions" class="px-2 py-1 whitespace-nowrap">
      <slot name="row-actions" :row="row"></slot>
    </td>
  </tr>
</tbody>

        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: "Danh sách" },
  data: { type: Array, default: () => [] },
  columns: { type: Array, default: () => [] }, // [{label: "Tên cột", field: "firstName"}]
  idKey: { type: String, default: "id" },
  hasActions: { type: Boolean, default: false }
})
</script>
