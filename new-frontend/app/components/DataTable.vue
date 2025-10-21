<template>
  <div class="w-full mx-auto px-4 sm:px-6 ">
    <div class="bg-white shadow-md rounded-lg overflow-hidden border border-gray-200 max-w-full ">
      
      <!-- Header (fixed, không scroll) -->
      <div class="flex flex-wrap justify-between items-center bg-gray-50 border-b border-gray-200 px-6 py-4 gap-2 ">
        <h2 class="text-xl font-semibold text-gray-800">{{ title }}</h2>
        <div class="flex gap-2 flex-wrap ">
          <CButton 
            v-if="showAddButton"
            :to="addButtonTo"
            variant="primary"
          >
            {{ addLabel }}
          </CButton>

          <CButton
            v-if="showRegisterButton"
            :to="registerTo"
            variant="register"
            @click="handleRegister"
          >
            {{ registerLabel }}
          </CButton>
          
          <CButton 
            v-if="showEditButton && isAdmin"
            variant="edit" 
            :disabled="!selectedRow" 
            @edit="handleEdit" 
          >
            {{ editLabel }}
          </CButton>

          <CButton 
            v-if="!registerMode && !hideDeleteButton"
            variant="delete" 
            :disabled="!selectedRow" 
            @delete="handleDelete" 
          >
            {{ deleteLabel }}
          </CButton>
        </div>
      </div>

      <!-- Table Wrapper (chỉ phần này scroll) -->
      <div class="hidden lg:block border-t border-b border-gray-200 max-w-full *:h-full">
        <div class="overflow-x-auto overflow-y-auto" :style="{ 'max-height': maxHeight }">
          <table class="w-full border-separate border-spacing-0 table-fixed">
            <thead class="bg-gray-200">
              <tr>
                <th
                  v-for="(col, index) in columns"
                  :key="index"
                  @click="sortBy(col.field)"
                  class="px-3 py-3 text-xs sm:text-sm font-semibold text-gray-700 text-left cursor-pointer select-none border-b border-gray-200 hover:bg-gray-300 transition-colors sticky top-0 z-10"
                  :style="getColumnStyle(col.field)"
                >
                  <div class="flex items-center gap-1">
                    <span class="truncate">{{ col.label }}</span>
                    <span class="text-gray-400 text-sm flex-shrink-0">
                      <template v-if="sortField === col.field">
                        <span v-if="sortOrder === 'asc'">↑</span>
                        <span v-else>↓</span>
                      </template>
                      <template v-else>⇅</template>
                    </span>
                  </div>
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="(row, idx) in sortedData"
                :key="row[idKey]"
                @click="selectRow(row)"
                class="text-sm text-gray-700 border-b border-gray-100 transition-all duration-200"
                :class="[ 
                  selectedRow && selectedRow[idKey] === row[idKey]
                    ? 'bg-blue-100 border-l-4 border-blue-500 hover:bg-blue-100'
                    : idx % 2 === 0
                    ? 'bg-white hover:bg-blue-50 cursor-pointer'
                    : 'bg-gray-50 hover:bg-blue-50 cursor-pointer'
                ]"
              >
                <td
                  v-for="(col, index) in columns"
                  :key="index"
                  class="px-3 py-2 text-left text-xs sm:text-sm truncate"
                  :style="getColumnStyle(col.field)"
                >
                  <div class="truncate" :title="row[col.field]">
                    {{ row[col.field] }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Card View (Mobile) -->
      <div class="lg:hidden space-y-4 p-6 overflow-y-auto" :style="{ 'max-height': maxHeight }">
        <div
          v-for="(row, idx) in sortedData"
          :key="row[idKey]"
          @click="selectRow(row)"
          class="border border-gray-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
          :class="[ 
            selectedRow && selectedRow[idKey] === row[idKey]
              ? 'border-blue-500 bg-blue-50'
              : 'hover:border-gray-300'
          ]"
        >
          <div class="space-y-3">
            <div v-for="(col, index) in priorityColumns" :key="index" class="flex justify-between">
              <span class="font-medium text-gray-600 text-base">{{ col.label }}:</span>
              <span class="text-gray-900 text-base text-right">{{ row[col.field] }}</span>
            </div>
            
            <div v-if="expandedRows[row[idKey]]" class="pt-3 border-t border-gray-200">
              <div v-for="(col, index) in secondaryColumns" :key="index" class="flex justify-between py-1">
                <span class="font-medium text-gray-600 text-base">{{ col.label }}:</span>
                <span class="text-gray-900 text-base text-right">{{ row[col.field] }}</span>
              </div>
            </div>
            
            <button
              @click.stop="toggleExpand(row[idKey])"
              class="text-blue-600 text-base hover:text-blue-800 transition-colors"
            >
              {{ expandedRows[row[idKey]] ? 'Thu gọn' : 'Xem thêm' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import CButton from './CButton.vue'

const props = defineProps({
  title: { type: String, default: 'Danh sách' },
  data: { type: Array, default: () => [] },
  columns: { type: Array, default: () => [] },
  idKey: { type: String, default: 'id' },
  editLabel: { type: String, default: 'Sửa' },
  deleteLabel: { type: String, default: 'Xóa' },
  hideDeleteButton: { type: Boolean, default: false },
  addLabel: { type: String, default: 'Thêm' },
  showAddButton: { type: Boolean, default: false },
  addButtonTo: { type: String, default: '' },
  showRegisterButton: { type: Boolean, default: false },
  registerLabel: { type: String, default: 'Đăng ký' },
  registerTo: { type: String, default: '' },
  registerMode: { type: Boolean, default: false },
  showEditButton: { type: Boolean, default: true },
  isAdmin: { type: Boolean, default: false },
  maxHeight: { type: String, default: '85%' }
})

const selectedRow = ref(null)
const sortField = ref(null)
const sortOrder = ref('asc')
const expandedRows = ref({})
const emit = defineEmits(['edit', 'delete', 'register'])

const handleRegister = () => emit('register', selectedRow.value)
const handleEdit = () => selectedRow.value && emit('edit', selectedRow.value)
const handleDelete = () => selectedRow.value && emit('delete', selectedRow.value)

const selectRow = (row) => {
  selectedRow.value =
    selectedRow.value && selectedRow.value[props.idKey] === row[props.idKey]
      ? null
      : row
}

const sortBy = (field) => {
  if (sortField.value === field)
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
}

const toggleExpand = (id) => {
  expandedRows.value[id] = !expandedRows.value[id]
}

const getColumnStyle = (field) => {
  const widths = {
    teacherCode: '8%',
    studentCode: '8%',
    lastName: '12%',
    firstName: '10%',
    dob: '10%',
    gender: '6%',
    email: '14%',
    phone: '10%',
    faculty: '10%',
    department: '10%',
    specialization: '12%',
    degree: '8%',
    academicRank: '10%',
    className: '8%',
    status: '8%'
  }
  return { width: widths[field] || '10%' }
}

const priorityColumns = computed(() => {
  const priority = ['teacherCode', 'studentCode', 'lastName', 'firstName', 'email']
  return props.columns.filter(col => priority.includes(col.field))
})

const secondaryColumns = computed(() => {
  const priority = ['teacherCode', 'studentCode', 'lastName', 'firstName', 'email']
  return props.columns.filter(col => !priority.includes(col.field))
})

const sortedData = computed(() => {
  if (!sortField.value) return props.data
  return [...props.data].sort((a, b) => {
    const aVal = a[sortField.value]
    const bVal = b[sortField.value]
    if (aVal == null || bVal == null) return 0
    if (typeof aVal === 'number' && typeof bVal === 'number')
      return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal
    return sortOrder.value === 'asc'
      ? String(aVal).localeCompare(String(bVal))
      : String(bVal).localeCompare(String(aVal))
  })
})
</script>

<style scoped>
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}
.overflow-x-auto::-webkit-scrollbar {
  height: 8px;
  width: 8px;
}
.overflow-x-auto::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 4px;
}
.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 4px;
}
.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
thead th {
  background-color: #e5e7eb;
}
table {
  table-layout: fixed;
}
</style>
