<template>
  <div class="flex flex-col h-screen bg-gradient-to-br from-blue-500 to-purple-600">
    <div class="m-2 flex-1 bg-white bg-opacity-95 backdrop-blur-xl rounded-lg shadow-2xl overflow-hidden">
      <!-- Header -->
      <header class="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-5 rounded-t-lg relative overflow-hidden">
        <div class="flex justify-between items-center relative z-10">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-white bg-opacity-20 rounded-lg flex items-center justify-center backdrop-blur border border-white border-opacity-30">
              <FeatherIcon name="box" class="w-6 h-6" />
            </div>
            <div>
              <h1 class="text-2xl font-bold">{{ diagram.title || 'Untitled Diagram' }}</h1>
              <p class="text-sm opacity-90">Visual Diagram Editor</p>
            </div>
          </div>
          <div class="flex gap-3">
            <Button
              appearance="white"
              @click="undo"
              :disabled="!canUndo"
            >
              <template #prefix>
                <FeatherIcon name="rotate-ccw" class="w-4 h-4" />
              </template>
              Undo
            </Button>
            <Button
              appearance="white"
              @click="redo"
              :disabled="!canRedo"
            >
              <template #prefix>
                <FeatherIcon name="rotate-cw" class="w-4 h-4" />
              </template>
              Redo
            </Button>
            <Button
              appearance="primary"
              :loading="saving"
              @click="saveDiagram"
            >
              <template #prefix>
                <FeatherIcon name="save" class="w-4 h-4" />
              </template>
              Save
            </Button>
            <Button
              appearance="white"
              @click="showExportMenu = true"
            >
              <template #prefix>
                <FeatherIcon name="download" class="w-4 h-4" />
              </template>
              Export
            </Button>
            <Button
              appearance="white"
              @click="showShareMenu = true"
            >
              <template #prefix>
                <FeatherIcon name="share-2" class="w-4 h-4" />
              </template>
              Share
            </Button>
          </div>
        </div>
      </header>

      <!-- Toolbar -->
      <div class="bg-gray-50 px-4 py-2 border-b border-gray-200 flex items-center gap-4">
        <Select
          v-model="diagram.type"
          :options="diagramTypes"
          class="w-48"
          @change="handleDiagramTypeChange"
        />
        <Select
          v-model="diagram.theme"
          :options="mermaidThemes"
          class="w-48"
          @change="handleThemeChange"
        />
        <div class="flex-1"></div>
        <Button
          appearance="minimal"
          @click="insertNode"
        >
          <template #prefix>
             <FeatherIcon name="circle" class="w-4 h-4" />
          </template>
          Add Node
        </Button>
        <Button
          appearance="minimal"
          @click="insertEdge"
        >
          <template #prefix>
            <FeatherIcon name="arrow-right" class="w-4 h-4" />
          </template>
          Add Edge
        </Button>
        <Button
          appearance="minimal"
          @click="insertSubgraph"
        >
          <template #prefix>
            <FeatherIcon name="box" class="w-4 h-4" />
          </template>
          Add Subgraph
        </Button>
      </div>

      <!-- Main Content -->
      <div class="flex flex-1 h-[calc(100vh-14rem)]">
        <!-- Editor Panel -->
        <div class="flex-1 flex flex-col bg-gray-900">
          <div class="bg-gray-800 text-white px-5 py-3 flex justify-between items-center border-b border-gray-700">
            <h3 class="font-medium flex items-center gap-2">
              <FeatherIcon name="code" class="w-4 h-4" />
              Mermaid Code
            </h3>
            <div class="text-sm text-gray-400">
              {{ editorStats }}
            </div>
          </div>
          <div ref="monacoContainer" class="flex-1"></div>
        </div>

        <!-- Preview Panel -->
        <div class="flex-1 flex flex-col bg-white border-l border-gray-200">
          <div class="bg-gray-50 px-5 py-3 flex justify-between items-center border-b border-gray-200">
            <h3 class="font-medium flex items-center gap-2">
              <FeatherIcon name="eye" class="w-4 h-4" />
              Live Preview
            </h3>
            <div class="flex items-center gap-2">
              <Button
                appearance="minimal"
                @click="zoomOut"
              >
                <FeatherIcon name="minus" class="w-4 h-4" />
              </Button>
              <span class="text-sm font-medium w-16 text-center">
                {{ Math.round(zoom * 100) }}%
              </span>
              <Button
                appearance="minimal"
                @click="zoomIn"
              >
                <FeatherIcon name="plus" class="w-4 h-4" />
              </Button>
              <Button
                appearance="minimal"
                @click="resetZoom"
              >
                <FeatherIcon name="maximize" class="w-4 h-4" />
              </Button>
            </div>
          </div>
          <div 
            class="flex-1 p-8 overflow-auto bg-grid"
            @wheel.ctrl.prevent="handleWheel"
          >
            <div 
              class="mermaid-preview"
              :style="{ transform: `scale(${zoom})` }"
              v-html="renderedDiagram"
            ></div>
            <div v-if="renderError" class="error-message">
              {{ renderError }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Export Menu -->
    <Dialog v-model="showExportMenu" title="Export Diagram">
      <div class="space-y-4">
        <Button
          appearance="primary"
          class="w-full"
          @click="exportAsSVG"
        >
          <template #prefix>
            <FeatherIcon name="image" class="w-4 h-4" />
          </template>
          Export as SVG
        </Button>
        <Button
          appearance="primary"
          class="w-full"
          @click="exportAsPNG"
        >
          <template #prefix>
            <FeatherIcon name="image" class="w-4 h-4" />
          </template>
          Export as PNG
        </Button>
        <Button
          appearance="primary"
          class="w-full"
          @click="exportAsPDF"
        >
          <template #prefix>
            <FeatherIcon name="file" class="w-4 h-4" />
          </template>
          Export as PDF
        </Button>
      </div>
    </Dialog>

    <!-- Share Menu -->
    <Dialog v-model="showShareMenu" title="Share Diagram">
      <div class="space-y-4">
        <Input
          v-model="shareLink"
          label="Share Link"
          readonly
        />
        <div class="flex gap-2">
          <Button
            appearance="primary"
            class="flex-1"
            @click="copyShareLink"
          >
            <template #prefix>
              <FeatherIcon name="copy" class="w-4 h-4" />
            </template>
            Copy Link
          </Button>
          <Button
            appearance="primary"
            class="flex-1"
            @click="generateQRCode"
          >
            <template #prefix>
              <FeatherIcon name="qr-code" class="w-4 h-4" />
            </template>
            Show QR Code
          </Button>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { createApp } from '@vue/runtime-dom'
import { Button, FeatherIcon, Select, Dialog, Input, toast } from 'frappe-ui'

// References for dependencies
const monaco = ref(null)
const mermaid = ref(null)
const html2canvas = ref(null)
const jsPDF = ref(null)

// Load dependencies on mount
onMounted(async () => {
  try {
    // Wait for Monaco editor to be available
    while (!window.monaco) {
      await new Promise(resolve => setTimeout(resolve, 100))
    }
    monaco.value = window.monaco
    
    // Wait for Mermaid to be available
    while (!window.mermaid) {
      await new Promise(resolve => setTimeout(resolve, 100))
    }
    mermaid.value = window.mermaid
    
    // Load export utilities dynamically
    html2canvas.value = (await import('html2canvas')).default
    jsPDF.value = (await import('jspdf')).default
    
    
    // Initialize editor after dependencies are loaded
    initializeEditor()
  } catch (error) {
    console.error('Error initializing editor:', error)
  }
})

// State
const diagram = ref({
  title: '',
  type: 'flowchart',
  theme: 'default',
  code: `graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[Alternative]
    C --> E[End]
    D --> E`,
  doctype: null,
})
const monacoContainer = ref(null)
const editor = ref(null)
const zoom = ref(1)
const renderedDiagram = ref('')
const renderError = ref(null)
const saving = ref(false)
const showExportMenu = ref(false)
const showShareMenu = ref(false)
const shareLink = ref('')
const history = ref([])
const historyIndex = ref(-1)

// Diagram types and templates
const diagramTypes = [
  { label: 'Flowchart', value: 'flowchart' },
  { label: 'Sequence Diagram', value: 'sequence' },
  { label: 'Class Diagram', value: 'class' },
  { label: 'State Diagram', value: 'state' },
  { label: 'Entity Relationship', value: 'er' },
  { label: 'User Journey', value: 'journey' },
  { label: 'Gantt Chart', value: 'gantt' },
  { label: 'Pie Chart', value: 'pie' },
]

const mermaidThemes = [
  { label: 'Default', value: 'default' },
  { label: 'Forest', value: 'forest' },
  { label: 'Dark', value: 'dark' },
  { label: 'Neutral', value: 'neutral' },
]

// Templates for different diagram types
const templates = {
  flowchart: `graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[Alternative]
    C --> E[End]
    D --> E`,
  sequence: `sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!`,
  class: `classDiagram
    Class01 <|-- AveryLongClass : Cool
    Class03 *-- Class04
    Class05 o-- Class06
    Class07 .. Class08
    Class09 --> C2 : Where am i?
    Class09 --* C3
    Class09 --|> Class07
    Class07 : equals()
    Class07 : Object[] elementData
    Class01 : size()
    Class01 : int chimp
    Class01 : int gorilla
    Class08 <--> C2: Cool label`,
  state: `stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]`,
  er: `erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses`,
  journey: `journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me`,
  gantt: `gantt
    title A Gantt Chart
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2014-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2014-01-12  , 12d
    another task      : 24d`,
  pie: `pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 85
    "Rats" : 15`
}

// Editor stats
const editorStats = computed(() => {
  if (!editor.value) return ''
  const model = editor.value.getModel()
  const lines = model.getLineCount()
  const chars = model.getValueLength()
  return `${lines} lines, ${chars} characters`
})

// Undo/Redo state
const canUndo = computed(() => historyIndex.value > 0)
const canRedo = computed(() => historyIndex.value < history.value.length - 1)

// Monaco editor setup
function initializeEditor() {
  editor.value = monaco.value.editor.create(monacoContainer.value, {
    value: diagram.value.code,
    language: 'markdown',
    theme: 'vs-dark',
    minimap: { enabled: false },
    fontSize: 14,
    fontFamily: '"Fira Code", Consolas, Monaco, monospace',
    lineNumbers: 'on',
    roundedSelection: true,
    scrollBeyondLastLine: false,
    automaticLayout: true,
  })

  // Add keyboard shortcuts
  editor.value.addCommand(monaco.value.KeyMod.CtrlCmd | monaco.value.KeyCode.KeyS, () => {
    saveDiagram()
  })

  // Update preview on content change
  editor.value.onDidChangeModelContent(debounce(() => {
    const newCode = editor.value.getValue()
    if (newCode !== diagram.value.code) {
      addToHistory(newCode)
      diagram.value.code = newCode
      renderDiagram()
    }
  }, 300))

  // Initial render
  renderDiagram()
}

// Handle diagram type change
function handleDiagramTypeChange() {
  diagram.value.code = templates[diagram.value.type]
  editor.value.setValue(diagram.value.code)
  addToHistory(diagram.value.code)
}

// Handle theme change
function handleThemeChange() {
  mermaid.value.initialize({
    startOnLoad: false,
    theme: diagram.value.theme,
    securityLevel: 'loose',
  })
  renderDiagram()
}

// Insert diagram elements
function insertNode() {
  const selection = editor.value.getSelection()
  const position = selection ? selection.getPosition() : editor.value.getPosition()
  const nodeText = prompt('Enter node text:')
  if (nodeText) {
    const nodeId = 'node' + Date.now()
    const nodeCode = `    ${nodeId}[${nodeText}]`
    editor.value.executeEdits('', [{
      range: new monaco.value.Range(position.lineNumber, 1, position.lineNumber, 1),
      text: nodeCode + '\n',
      forceMoveMarkers: true
    }])
  }
}

function insertEdge() {
  const selection = editor.value.getSelection()
  const position = selection ? selection.getPosition() : editor.value.getPosition()
  const fromNode = prompt('Enter source node ID:')
  const toNode = prompt('Enter target node ID:')
  if (fromNode && toNode) {
    const edgeCode = `    ${fromNode} --> ${toNode}`
    editor.value.executeEdits('', [{
      range: new monaco.value.Range(position.lineNumber, 1, position.lineNumber, 1),
      text: edgeCode + '\n',
      forceMoveMarkers: true
    }])
  }
}

function insertSubgraph() {
  const selection = editor.value.getSelection()
  const position = selection ? selection.getPosition() : editor.value.getPosition()
  const subgraphName = prompt('Enter subgraph name:')
  if (subgraphName) {
    const subgraphCode = `    subgraph ${subgraphName}\n    end`
    editor.value.executeEdits('', [{
      range: new monaco.value.Range(position.lineNumber, 1, position.lineNumber, 1),
      text: subgraphCode + '\n',
      forceMoveMarkers: true
    }])
  }
}

// History management
function addToHistory(code) {
  history.value = history.value.slice(0, historyIndex.value + 1)
  history.value.push(code)
  historyIndex.value = history.value.length - 1
}

function undo() {
  if (canUndo.value) {
    historyIndex.value--
    editor.value.setValue(history.value[historyIndex.value])
  }
}

function redo() {
  if (canRedo.value) {
    historyIndex.value++
    editor.value.setValue(history.value[historyIndex.value])
  }
}

// Render mermaid diagram
async function renderDiagram() {
  try {
    renderError.value = null
    const { svg } = await mermaid.value.render(
      'mermaid-' + Date.now(),
      diagram.value.code
    )
    renderedDiagram.value = svg
  } catch (error) {
    renderError.value = error.message
    console.error('Mermaid rendering error:', error)
  }
}

// Save diagram
async function saveDiagram() {
  saving.value = true
  try {
    if (diagram.value.doctype) {
      await window.frappe.call({
        method: 'frappe.client.set_value',
        args: {
          doctype: 'Mermaid Diagram',
          name: diagram.value.doctype,
          fieldname: {
            title: diagram.value.title || 'Untitled Diagram',
            code: diagram.value.code,
            type: diagram.value.type,
            theme: diagram.value.theme,
          }
        }
      })
      toast.success('Diagram saved successfully')
    } else {
      const result = await window.frappe.call({
        method: 'frappe.client.insert',
        args: {
          doc: {
            doctype: 'Mermaid Diagram',
            title: diagram.value.title || 'Untitled Diagram',
            code: diagram.value.code,
            type: diagram.value.type,
            theme: diagram.value.theme,
          }
        }
      })
      diagram.value.doctype = result.message.name
      toast.success('Diagram created successfully')
    }
  } catch (error) {
    console.error('Error saving diagram:', error)
    toast.error('Failed to save diagram')
  } finally {
    saving.value = false
  }
}

// Export functions
async function exportAsSVG() {
  const svg = document.querySelector('.mermaid-preview svg')
  if (svg) {
    const svgData = new XMLSerializer().serializeToString(svg)
    const blob = new Blob([svgData], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${diagram.value.title || 'diagram'}.svg`
    a.click()
    URL.revokeObjectURL(url)
  }
}

async function exportAsPNG() {
  const element = document.querySelector('.mermaid-preview')
  if (element) {
    const canvas = await html2canvas.value(element)
    const url = canvas.toDataURL('image/png')
    const a = document.createElement('a')
    a.href = url
    a.download = `${diagram.value.title || 'diagram'}.png`
    a.click()
  }
}

async function exportAsPDF() {
  const element = document.querySelector('.mermaid-preview')
  if (element) {
    const canvas = await html2canvas.value(element)
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF.value({
      orientation: 'landscape',
      unit: 'px',
      format: [canvas.width, canvas.height]
    })
    pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height)
    pdf.save(`${diagram.value.title || 'diagram'}.pdf`)
  }
}

// Share functions
function copyShareLink() {
  if (diagram.value.doctype) {
    const url = `${window.location.origin}/app/mermaid-diagram/${diagram.value.doctype}`
    navigator.clipboard.writeText(url)
    toast.success('Share link copied to clipboard')
  }
}

function generateQRCode() {
  if (diagram.value.doctype) {
    const url = `${window.location.origin}/app/mermaid-diagram/${diagram.value.doctype}`
    // TODO: Implement QR code generation
    toast.info('QR code generation coming soon')
  }
}

// Zoom controls
function zoomIn() {
  zoom.value = Math.min(5, zoom.value + 0.1)
}

function zoomOut() {
  zoom.value = Math.max(0.1, zoom.value - 0.1)
}

function resetZoom() {
  zoom.value = 1
}

function handleWheel(event) {
  if (event.deltaY < 0) {
    zoomIn()
  } else {
    zoomOut()
  }
}

// Utility functions
function debounce(fn, delay) {
  let timeoutId
  return function (...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn.apply(this, args), delay)
  }
}
</script>

<style>
.bg-grid {
  background-image: linear-gradient(rgba(0, 0, 0, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 0, 0, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}

.mermaid-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100%;
  transform-origin: center center;
}

.error-message {
  color: #ef4444;
  background-color: #fee2e2;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}
</style>
