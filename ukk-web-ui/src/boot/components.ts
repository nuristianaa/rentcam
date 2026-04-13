import { boot } from 'quasar/wrappers'

// LAYOUT
import PageLayout from '../components/layout/PageLayout.vue'
import HIndex from '../components/layout/HeaderIndex.vue'
import HForm from '../components/layout/HeaderForm.vue'
import HDetail from '../components/layout/HeaderDetail.vue'

// GENERAL
import JsonViewer from '../components/general/JsonViewer.vue'
import LogInfo from '../components/general/LogInfo.vue'
import LogDetails from '../components/general/LogDetails.vue'
import List from '../components/general/ListComponent.vue'
import LinkComponent from '../components/general/LinkComponent.vue'
import Loading from '../components/general/LoadingComponent.vue'
import DragNative from '../components/general/draggable/DragNativeComponent.vue'
import NestedDraggableFix from '../components/general/draggable/NestedDraggableFix.vue'
import TitleHead from '../components/general/TitleHead.vue'
import SBanner from '../components/general/SBanner.vue'
import GeneratePdf from '../components/general/GeneratePdf.vue'
import DownloadPdf from '../components/general/DownloadPdf.vue'
import MasterFiles from '../components/form/master-files/MasterFilesComponent.vue'
import FormCategories from '../components/form/categories/CategoryComponent.vue'
import HelpPopup from '../components/general/HelpPopup.vue'
import DocumentHistories from '../components/document-histories/DocumentHistories.vue'

import STable from '../components/table/IndexTableComponent.vue'
import RTable from '../components/table/IndexTblReportComponent.vue'
import PickerTable from '../components/table/IndexTblPickerComponent.vue'
import ApprovalForm from 'src/components/approval/ApprovalForm.vue'
import BannerLockApproval from 'src/components/approval/BannerLockApproval.vue'

// TASK and Notes
import TaskIndex from 'src/components/task/TaskIndex.vue'
import NotesIndex from 'src/components/notes/NotesIndex.vue'

// Modal
import Dialog from '../components/general/DialogComponent.vue'

// FORM
import Card from '../components/form/cards/CardComponent.vue'
import Tab from '../components/form/cards/TabComponent.vue'
import CategoryForm from 'src/components/form/CategoryForm.vue'
import DateForm from '../components/form/DateForm.vue'
import InputForm from '../components/form/InputForm.vue'
import NumberForm from '../components/form/NumberForm.vue'
import SelectForm from '../components/form/SelectForm.vue'
import TextareaForm from '../components/form/TextareaForm.vue'
import ToggleForm from '../components/form/ToggleForm.vue'
import UploaderForm from 'src/components/form/UploaderForm.vue'
import SelectionTable from 'src/components/form/SelectionTable.vue'
import InputColor from 'src/components/form/InputColor.vue'

import InputFormTable from '../components/form/form-table/InputFormTable.vue'
import NumberFormTable from '../components/form/form-table/NumberFormTable.vue'
import SelectFormTable from '../components/form/form-table/SelectFormTable.vue'
import SelectFormTableV2 from 'src/components/form/form-table/SelectFormTableV2.vue'
import FileFormTable from '../components/form/form-table/FileFormTable.vue'
import DateFormTable from '../components/form/form-table/DateFormTable.vue'

import DialogTableView from '../components/general/DialogTableView.vue'
import InputAutocompleteForm from 'src/components/form/InputAutocompleteForm.vue'
import AutocompleteTable from 'src/components/form/form-table/AutocompleteTable.vue'

import SChip from 'src/components/general/SChip.vue'

import QDraggableTree from 'src/components/general/QDraggableTree.vue'
import QDraggableTreeNode from 'src/components/general/QDraggableTreeNode.vue'
import ImageUploader from 'src/components/form/ImageUploader.vue'
import InputTag from 'src/components/form/InputTag.vue'

// we globally register our component with Vue
export default boot(({ app }: { app: any }) => {
  // Layout
  app.component('s-page', PageLayout)
  app.component('h-index', HIndex)
  app.component('h-form', HForm)
  app.component('h-detail', HDetail)
  // General
  app.component('json-viewer', JsonViewer)
  app.component('log-info', LogInfo)
  app.component('log-info-table', LogInfo)
  app.component('log-details', LogDetails)
  app.component('s-list', List)
  app.component('s-link', LinkComponent)
  app.component('s-loading', Loading)
  app.component('s-drag', DragNative)
  app.component('nested-draggable', NestedDraggableFix)
  app.component('s-title', TitleHead)
  app.component('s-banner', SBanner)
  app.component('gen-pdf', GeneratePdf)
  app.component('download-pdf', DownloadPdf)
  app.component('f-approval', ApprovalForm)
  app.component('task', TaskIndex)
  app.component('notes', NotesIndex)
  app.component('banner-lock-approval', BannerLockApproval)
  app.component('dialog-table', DialogTableView)
  app.component('help-popup', HelpPopup)
  app.component('document-histories', DocumentHistories)
  app.component('s-chip', SChip)
  app.component('q-draggable-tree', QDraggableTree)
  app.component('q-draggable-tree-node', QDraggableTreeNode)

  // Table
  app.component('s-table', STable)
  app.component('r-table', RTable)
  app.component('picker-table', PickerTable)

  // Modal
  app.component('s-dialog', Dialog)

  // Forms
  app.component('f-card', Card)
  app.component('f-tabs', Tab)
  app.component('f-category', CategoryForm)
  app.component('f-date', DateForm)
  app.component('f-input', InputForm)
  app.component('f-number', NumberForm)
  app.component('f-select', SelectForm)
  app.component('f-textarea', TextareaForm)
  app.component('f-toggle', ToggleForm)
  app.component('f-uploader', UploaderForm)
  app.component('f-image-uploader', ImageUploader)
  app.component('f-files', MasterFiles)
  app.component('f-categories', FormCategories)
  app.component('f-selection-table', SelectionTable)
  app.component('f-auto-complete', InputAutocompleteForm)
  app.component('f-input-tag', InputTag)
  app.component('f-color', InputColor)

  app.component('f-input-table', InputFormTable)
  app.component('f-number-table', NumberFormTable)
  app.component('f-select-table', SelectFormTable)
  app.component('f-select-table-2', SelectFormTableV2)
  app.component('f-file-table', FileFormTable)
  app.component('f-date-table', DateFormTable)
  app.component('f-auto-complete-table', AutocompleteTable)
})
