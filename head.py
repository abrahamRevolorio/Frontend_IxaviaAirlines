def addClientProtectionHead(ui):
    ui.add_head_html('''
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.1/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/toastify-js"></script>

    <style>
    .page-content { display: none; }
    </style>

    <script defer src="/static/auth.js"></script>  <!-- usa defer -->
    ''')
