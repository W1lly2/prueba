import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';                 // JS de Bootstrap
import './app.css';                 // <— TU CSS debe ir después

import App from './App.svelte';
new App({ target: document.getElementById('app')! })