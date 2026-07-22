export enum TipoCliente {
  NORMAL = 'NORMAL',
  ESPECIAL = 'ESPECIAL',
}

export enum TipoDia {
  ORDINARIO = 'ORDINARIO',
  FESTIVO = 'FESTIVO',
}

export enum TipoHorario {
  DIURNO = 'DIURNO',
  NOCTURNO = 'NOCTURNO',
}

export enum TipoServicio {
  AMBULANCIA_TAB = 'AMBULANCIA_TAB',
  AMBULANCIA_TAM = 'AMBULANCIA_TAM',
  AUXILIAR_ENFERMERIA = 'AUXILIAR_ENFERMERIA',
  PARAMEDICO = 'PARAMEDICO',
  CONDUCTOR_TAB = 'CONDUCTOR_TAB',
  CONDUCTOR_TAM = 'CONDUCTOR_TAM',
  MEDICO_GENERAL = 'MEDICO_GENERAL',
}

export enum TipoExtra {
  PEAJE = 'PEAJE',
  ALIMENTACION = 'ALIMENTACION',
  TRANSPORTE = 'TRANSPORTE',
  OTROS = 'OTROS',
}

export enum EstadoCotizacion {
  BORRADOR = 'BORRADOR',
  COTIZADA = 'COTIZADA',
  ENVIADA_CLIENTE = 'ENVIADA_CLIENTE',
  ACEPTADA_CLIENTE = 'ACEPTADA_CLIENTE',
  RECHAZADA_CLIENTE = 'RECHAZADA_CLIENTE',
  PENDIENTE_AREA_MEDICA = 'PENDIENTE_AREA_MEDICA',
  APROBADA_AREA_MEDICA = 'APROBADA_AREA_MEDICA',
  PROGRAMADA = 'PROGRAMADA',
  OC_SOLICITADA = 'OC_SOLICITADA',
  OC_RECIBIDA = 'OC_RECIBIDA',
  PENDIENTE_FACTURACION = 'PENDIENTE_FACTURACION',
  FACTURADA = 'FACTURADA',
  PAGADA = 'PAGADA',
  CERRADA = 'CERRADA',
}

export enum TipoInteraccionCRM {
  LLAMADA = 'LLAMADA',
  REUNION = 'REUNION',
  EMAIL = 'EMAIL',
  NOTA = 'NOTA',
  VISITA = 'VISITA',
}

export enum TipoAlerta {
  COTIZACION_SIN_RESPUESTA = 'COTIZACION_SIN_RESPUESTA',
  OC_DEMORADA = 'OC_DEMORADA',
  PAGO_PENDIENTE = 'PAGO_PENDIENTE',
  TAREA_VENCIDA = 'TAREA_VENCIDA',
  AREA_MEDICA_SIN_RESPUESTA = 'AREA_MEDICA_SIN_RESPUESTA',
  SERVICIO_HOY = 'SERVICIO_HOY',
}

export enum PrioridadTarea {
  BAJA = 'BAJA',
  MEDIA = 'MEDIA',
  ALTA = 'ALTA',
  CRITICA = 'CRITICA',
}

export enum OrigenFestivo {
  LIBRERIA = 'LIBRERIA',
  MANUAL = 'MANUAL',
}

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  activo: boolean;
  fechaCreacion: string;
}

export interface Ciudad {
  id: number;
  nombre: string;
  departamento: string;
  activo: boolean;
}

export interface Servicio {
  id: number;
  codigo: string;
  nombre: string;
  tipo: TipoServicio;
  activo: boolean;
}

export interface ContactoCliente {
  id: number;
  clienteId: number;
  nombre: string;
  cargo?: string;
  correo?: string;
  telefono?: string;
  esPrincipal: boolean;
  activo: boolean;
}

export interface Cliente {
  id: number;
  empresa: string;
  nit: string;
  correoPrincipal: string;
  telefonoPrincipal: string;
  tipoCliente: TipoCliente;
  sector?: string;
  ciudadId: number;
  direccion?: string;
  sitioWeb?: string;
  observaciones?: string;
  activo: boolean;
  fechaCreacion: string;
  usuarioCreadorId: number;
}

export interface InteraccionCRM {
  id: number;
  clienteId: number;
  cotizacionId?: number;
  tipo: TipoInteraccionCRM;
  fechaHora: string;
  asunto: string;
  descripcion?: string;
  usuarioId: number;
}

export interface Tarea {
  id: number;
  clienteId?: number;
  cotizacionId?: number;
  titulo: string;
  descripcion?: string;
  prioridad: PrioridadTarea;
  fechaVencimiento: string;
  completada: boolean;
  fechaCompletada?: string;
  usuarioAsignadoId: number;
  usuarioCreadorId: number;
}

export interface Tarifa {
  id: number;
  ciudadId: number;
  servicioId: number;
  tipoDia: TipoDia;
  tipoHorario: TipoHorario;
  clienteId: number | null; // null = General
  valorHora: number;
  vigenteDesde: string;
  vigenteHasta?: string | null;
  activo: boolean;
}

export interface Festivo {
  id: number;
  fecha: string; // YYYY-MM-DD
  nombre: string;
  origen: OrigenFestivo;
}

export interface ExtraEvento {
  id: number;
  eventoId?: number;
  tipo: TipoExtra;
  descripcion: string;
  valor: number;
}

export interface Evento {
  id: number;
  cotizacionId: number;
  servicioId: number;
  fecha: string; // YYYY-MM-DD
  horaInicio: string; // HH:mm
  horaFin: string; // HH:mm
  ciudadId: number;
  direccion: string;
  contacto: string;
  telefono: string;
  observaciones?: string;
  tipoDia: TipoDia; // Calculado
  horasDiurnas: number; // Calculado
  horasNocturnas: number; // Calculado
  valorHorasDiurnas: number; // Calculado
  valorHorasNocturnas: number; // Calculado
  valorExtras: number; // Suma extras
  valorEvento: number; // Total evento
  orden: number;
  extras: ExtraEvento[];
}

export interface Cotizacion {
  id: number;
  numeroCotizacion: string; // COT-2026-0001
  clienteId: number;
  contactoId?: number;
  estado: EstadoCotizacion;
  usuarioCreadorId: number;
  usuarioAsignadoId?: number;
  fechaCreacion: string;
  fechaEnviadaCliente?: string;
  fechaRespuestaCliente?: string;
  fechaEnviadaArea?: string;
  fechaAprobacionArea?: string;
  fechaProgramacion?: string;
  fechaOcSolicitada?: string;
  fechaOcRecibida?: string;
  fechaFacturacion?: string;
  fechaPago?: string;
  valorSubtotal: number;
  valorExtras: number;
  valorTotal: number;
  observaciones?: string;
  condicionesComerciales?: string;
  pdfPath?: string;
  eventos: Evento[];
}

export interface AreaMedica {
  id: number;
  nombre: string;
  correoContacto: string;
  telefono?: string;
  responsable?: string;
  activo: boolean;
}

export interface EnvioAreaMedica {
  id: number;
  cotizacionId: number;
  areaMedicaId: number;
  fechaEnvio: string;
  usuarioEnvioId: number;
  fechaRespuesta?: string;
  aprobado?: boolean;
  observacionesRespuesta?: string;
}

export interface Programacion {
  id: number;
  cotizacionId: number;
  eventoId: number;
  fechaProgramada: string;
  horaInicio: string;
  horaFin: string;
  recursoAsignado?: string; // Ej: Ambulancia TAB-04 + Dra. Elena
  notas?: string;
  outlookEventId?: string;
  estado: 'PENDIENTE' | 'CONFIRMADA' | 'REALIZADA' | 'CANCELADA';
}

export interface OrdenCompra {
  id: number;
  cotizacionId: number;
  numeroOc?: string;
  fechaSolicitud: string;
  fechaRecibido?: string;
  archivoPath?: string;
  observaciones?: string;
  estado: 'SOLICITADA' | 'RECIBIDA';
}

export interface Factura {
  id: number;
  cotizacionId: number;
  numeroFactura: string;
  fechaFacturacion: string;
  fechaVencimiento: string;
  fechaPago?: string;
  valorFacturado: number;
  observaciones?: string;
  estado: 'PENDIENTE' | 'FACTURADA' | 'PAGADA';
}

export interface Alerta {
  id: number;
  tipo: TipoAlerta;
  titulo: string;
  mensaje: string;
  entidadTipo: 'cotizacion' | 'tarea' | 'factura' | 'area_medica';
  entidadId: number;
  prioridad: 'INFO' | 'ADVERTENCIA' | 'CRITICA';
  fechaCreacion: string;
  fechaVisto?: string;
  usuarioId: number;
  activa: boolean;
}

export interface HistorialActividad {
  id: number;
  fechaHora: string;
  usuarioId: number;
  entidadTipo: string;
  entidadId: number;
  accion: string;
  detalle?: string;
  esAutomatico: boolean;
}

export interface ConfiguracionSistema {
  empresaNombre: string;
  empresaNit: string;
  empresaDireccion: string;
  empresaTelefono: string;
  empresaLogoPath: string;
  outlookCuentaEmail: string;
  pdfCondicionesGenerales: string;
  alertasDiasSinRespuesta: number;
  alertasDiasOcDemorada: number;
}
