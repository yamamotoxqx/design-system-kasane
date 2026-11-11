// Shareable config: { "extends": ["design-system-kasane/stylelint"] }
import { fileURLToPath } from 'node:url';

export default {
  plugins: [fileURLToPath(new URL('./plugin.js', import.meta.url))],
  rules: {
    'kasane/no-raw-color': true,
    'kasane/no-shadow': true,
    // Add your own input-like selectors if needed: [true, { "inputSelectors": ["\\.app-search"] }]
    'kasane/border-only-on-inputs': true,
    'kasane/use-tokens': [true, { severity: 'warning' }],
    'kasane/no-outline-none': true,
    'kasane/font-family-token': true,
  },
};
