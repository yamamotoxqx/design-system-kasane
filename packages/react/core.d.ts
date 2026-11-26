export interface Palette { id: string; name: string; en: string }
export declare const PALETTES: Palette[];
export type ToastType = 'ok' | 'info' | 'danger';
export interface ToastOptions {
  type?: ToastType;
  /** ms. Default 5000, 10000 with an action, 0 (stays until closed) for danger. */
  duration?: number;
  action?: { label: string; onClick?: () => void };
  closable?: boolean;
  /** Merge a repeat of the same message into the toast on screen ("×2"). Default true; never for danger or with an action. */
  merge?: boolean;
  closeLabel?: string;
  returnFocus?: HTMLElement;
  onClose?: () => void;
}
/** Show a toast at the bottom. It closes by itself (not errors) and pauses while hovered or focused. */
export declare function toast(message: string, options?: ToastOptions): { close(): void };
export declare function getAccent(): string;
/** Change the colour: repaints from the top (View Transitions) and saves it in localStorage. */
export declare function setAccent(id: string, options?: { save?: boolean; animate?: boolean }): void;
export declare function onAccent(fn: (accent: string) => void): () => void;
export declare function restoreAccent(): void;
export declare function recolor(update: () => void): void;
