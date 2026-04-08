{{/*
=============================================================
_helpers.tpl — Shared template helpers for BetMasterX chart
=============================================================
*/}}

{{/* Chart name */}}
{{- define "betmasterx.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Fully qualified release name */}}
{{- define "betmasterx.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/* Chart label */}}
{{- define "betmasterx.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Common labels */}}
{{- define "betmasterx.labels" -}}
helm.sh/chart: {{ include "betmasterx.chart" . }}
app.kubernetes.io/name: {{ include "betmasterx.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
environment: {{ .Values.global.environment }}
{{- end }}

{{/* Selector labels — backend */}}
{{- define "betmasterx.backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "betmasterx.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: backend
app: betmasterx-backend
{{- end }}

{{/* Selector labels — frontend */}}
{{- define "betmasterx.frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "betmasterx.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: frontend
app: betmasterx-frontend
{{- end }}

{{/* Backend image reference */}}
{{- define "betmasterx.backend.image" -}}
{{- printf "%s:%s" .Values.backend.image.repository .Values.backend.image.tag }}
{{- end }}

{{/* Frontend image reference */}}
{{- define "betmasterx.frontend.image" -}}
{{- printf "%s:%s" .Values.frontend.image.repository .Values.frontend.image.tag }}
{{- end }}
