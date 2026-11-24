import * as React from 'react';
export * from './core.js';
import type { ToastOptions } from './core.js';

type Icon = string | React.ReactNode;
type Div = React.HTMLAttributes<HTMLDivElement>;

export declare function Icon(props: { name: 'check' | 'circle-alert' | 'info' | 'x' | 'menu' | 'search'; className?: string }): React.ReactElement | null;

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'quiet' | 'danger';
  size?: 'sm' | 'lg';
  /** A Kasane icon name or an element (e.g. from lucide-react). Without children it becomes an icon button: add aria-label. */
  icon?: Icon;
  href?: string;
}
export declare const Button: React.ForwardRefExoticComponent<ButtonProps & React.RefAttributes<HTMLButtonElement>>;

interface FieldProps {
  label?: React.ReactNode;
  hint?: React.ReactNode;
  error?: React.ReactNode;
  /** An icon at the start (e.g. "search") */
  start?: Icon;
  /** A unit at the end (e.g. "円") */
  end?: React.ReactNode;
  fieldClassName?: string;
}
export type TextFieldProps = FieldProps & React.InputHTMLAttributes<HTMLInputElement>;
export declare const TextField: React.ForwardRefExoticComponent<TextFieldProps & React.RefAttributes<HTMLInputElement>>;
export declare const DateField: React.ForwardRefExoticComponent<TextFieldProps & { type?: 'date' | 'time' | 'datetime-local' | 'month' | 'week' } & React.RefAttributes<HTMLInputElement>>;
export declare const SearchField: React.ForwardRefExoticComponent<TextFieldProps & React.RefAttributes<HTMLInputElement>>;
export declare const TextArea: React.ForwardRefExoticComponent<FieldProps & React.TextareaHTMLAttributes<HTMLTextAreaElement> & React.RefAttributes<HTMLTextAreaElement>>;
export declare const Select: React.ForwardRefExoticComponent<FieldProps & React.SelectHTMLAttributes<HTMLSelectElement> & { options?: { value: string; label: React.ReactNode; disabled?: boolean }[] } & React.RefAttributes<HTMLSelectElement>>;
export declare function DateRange(props: { legend: React.ReactNode; start: TextFieldProps; end: TextFieldProps; type?: 'date' | 'time' | 'datetime-local' | 'month'; separator?: string; className?: string }): React.ReactElement;

type OptionProps = React.InputHTMLAttributes<HTMLInputElement> & { label?: React.ReactNode };
export declare const Checkbox: React.ForwardRefExoticComponent<OptionProps & React.RefAttributes<HTMLInputElement>>;
export declare const Radio: React.ForwardRefExoticComponent<OptionProps & React.RefAttributes<HTMLInputElement>>;
export declare const Switch: React.ForwardRefExoticComponent<OptionProps & React.RefAttributes<HTMLInputElement>>;

export declare function Card(props: Div & { title?: React.ReactNode; titleAs?: string; text?: React.ReactNode }): React.ReactElement;
export declare function Nest(props: Div): React.ReactElement;
export declare function Notice(props: Div & { title?: React.ReactNode; titleAs?: string }): React.ReactElement;
export declare function List(props: React.HTMLAttributes<HTMLUListElement>): React.ReactElement;
export declare function ListItem(props: React.LiHTMLAttributes<HTMLLIElement> & { main: React.ReactNode; sub?: React.ReactNode }): React.ReactElement;
export declare function Badge(props: React.HTMLAttributes<HTMLSpanElement> & { tone?: 'accent' | 'ok' | 'danger' | 'info' }): React.ReactElement;

export interface Tab { id: string; label: React.ReactNode; content?: React.ReactNode }
export declare function Tabs(props: { label: string; tabs: Tab[]; value?: string; defaultValue?: string; onChange?: (id: string) => void; className?: string }): React.ReactElement;
export declare function Segmented<T extends string>(props: { label: string; options: { value: T; label: React.ReactNode }[]; value: T; onChange?: (value: T) => void; className?: string }): React.ReactElement;
export declare function Progress(props: { label: string; value: number; max?: number }): React.ReactElement;
export declare function Dialog(props: { open: boolean; onClose?: () => void; title: React.ReactNode; text?: React.ReactNode; actions?: React.ReactNode; children?: React.ReactNode; className?: string }): React.ReactElement | null;

export declare function useAccent(): [string, (id: string, options?: { save?: boolean; animate?: boolean }) => void];
export declare function Palette(props: { legend?: string; compact?: boolean; name?: string; lang?: 'ja' | 'en'; className?: string }): React.ReactElement;

export interface AppShellProps {
  brand: React.ReactNode;
  brandHref?: string;
  brandAs?: React.ElementType;
  logo?: React.ReactNode;
  actions?: React.ReactNode;
  /** Links in the header (sites with five pages or fewer; use with single) */
  headerNav?: React.ReactNode;
  /** The sidebar content (NavGroup / NavLink). Under 900px it becomes the menu drawer. */
  sidebar?: React.ReactNode;
  footer?: React.ReactNode;
  single?: boolean;
  plain?: boolean;
  lang?: 'ja' | 'en';
  menuLabel?: string;
  closeLabel?: string;
  navLabel?: string;
  className?: string;
  children?: React.ReactNode;
}
export declare function AppShell(props: AppShellProps): React.ReactElement;
export declare function NavGroup(props: { title?: React.ReactNode; className?: string; children?: React.ReactNode }): React.ReactElement;
export declare function NavLink(props: React.AnchorHTMLAttributes<HTMLAnchorElement> & { as?: React.ElementType; current?: boolean; icon?: Icon; badge?: React.ReactNode; [key: string]: unknown }): React.ReactElement;
export declare function Breadcrumb(props: { items: { label: React.ReactNode; href?: string }[]; label?: string; lang?: 'ja' | 'en'; linkAs?: React.ElementType }): React.ReactElement;
export declare function Footer(props: { links?: { label: React.ReactNode; href: string }[]; linksLabel?: string; palette?: boolean; note?: React.ReactNode; lang?: 'ja' | 'en'; linkAs?: React.ElementType; className?: string; children?: React.ReactNode }): React.ReactElement;

export interface Column<R> { key: string; label: React.ReactNode; numeric?: boolean; render?: (row: R) => React.ReactNode }
export declare function Table<R extends Record<string, unknown>>(props: { caption?: React.ReactNode; label?: string; columns: Column<R>[]; rows: R[]; rowKey?: keyof R & string; className?: string }): React.ReactElement;
export declare function Empty(props: { icon?: Icon; title: React.ReactNode; titleAs?: string; text?: React.ReactNode; children?: React.ReactNode; className?: string }): React.ReactElement;
export declare function Skeleton(props: { lines?: number; title?: boolean; card?: boolean; label?: string; lang?: 'ja' | 'en'; className?: string }): React.ReactElement;

export declare function useToast(): (message: string, options?: ToastOptions) => { close(): void };
