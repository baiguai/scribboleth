const fs = require('fs');
const path = require('path');
const http = require('http');

function extract(text, regex, def) {
    const m = text.match(regex);
    return m ? m[1] : def;
}

function extractAll(text, regex) {
    const results = [];
    let m;
    while ((m = regex.exec(text)) !== null) {
        results.push(m[1] !== undefined ? m[1] : m[0]);
    }
    return results;
}

function main() {
    const args = process.argv.slice(2);
    if (args.length < 1) {
        console.error('Usage: node update-helper.js <instance-path> [template-path]');
        process.exit(1);
    }

    const instancePath = args[0];
    const templatePath = args[1] || null;

    if (!fs.existsSync(instancePath)) {
        console.error('Instance not found:', instancePath);
        process.exit(1);
    }

    const instanceContent = fs.readFileSync(instancePath, 'utf8');

    const nodePortStr = extract(instanceContent, /let\s+nodePort\s*=\s*(\d+);/, '0');
    const nodePort = parseInt(nodePortStr, 10);

    const fileName = extract(instanceContent, /let\s+fileName\s*=\s*"([^"]*)";/, 'help');

    const editorContent = extract(instanceContent, /<textarea[^>]*>([\s\S]*?)<\/textarea>/, '');

    const treeData = extract(instanceContent, /let\s+treeData\s*=\s*([\s\S]*?);\s*\n\s*let\s+bookmarks\s*=/, '[]');
    const bookmarks = extract(instanceContent, /let\s+bookmarks\s*=\s*([\s\S]*?);\s*\n\s*let\s+historyStack\s*=/, '[]');
    const historyStack = extract(instanceContent, /let\s+historyStack\s*=\s*([\s\S]*?);\s*\n/, '[]');
    const currentTheme = extract(instanceContent, /let\s+currentTheme\s*=\s*(null|[\s\S]*?);\s*\n/, 'null');

    const showInitHelp = extract(instanceContent, /let\s+showInitHelp\s*=\s*(true|false);/, 'false');
    const headerTemplate = extract(instanceContent, /let\s+headerTemplate\s*=\s*"([^"]*)";/, '__| ^*^ |__');
    const mode_vim = extract(instanceContent, /let\s+mode_vim\s*=\s*(true|false);/, 'true');

    const documentTitle = extract(instanceContent, /<title>([^<]*)<\/title>/, fileName);

    const template = templatePath
        ? fs.readFileSync(templatePath, 'utf8')
        : instanceContent;

    let result = template;

    result = result.replace(
        /let\s+fileName\s*=\s*"([^"]*)";/,
        `let fileName = "${fileName}";`
    );
    result = result.replace(
        /let\s+showInitHelp\s*=\s*(true|false);/,
        `let showInitHelp = ${showInitHelp};`
    );
    result = result.replace(
        /let\s+mode_vim\s*=\s*(true|false);/,
        `let mode_vim = ${mode_vim};`
    );
    result = result.replace(
        /let\s+nodePort\s*=\s*\d+;/,
        `let nodePort = ${nodePort};`
    );
    result = result.replace(
        /let\s+headerTemplate\s*=\s*"([^"]*)";/,
        `let headerTemplate = "${headerTemplate}";`
    );
    result = result.replace(
        /let\s+treeData\s*=\s*\[[\s\S]*?\];/,
        'let treeData = ' + treeData + ';'
    );
    result = result.replace(
        /let\s+bookmarks\s*=\s*\[[\s\S]*?\];/,
        'let bookmarks = ' + bookmarks + ';'
    );
    result = result.replace(
        /let\s+historyStack\s*=\s*\[[\s\S]*?\];/,
        'let historyStack = ' + historyStack + ';'
    );
    result = result.replace(
        /let\s+currentTheme\s*=\s*(null|\[[\s\S]*?\]);/,
        'let currentTheme = ' + currentTheme + ';'
    );
    result = result.replace(
        /<title>[^<]*<\/title>/,
        `<title>${documentTitle}</title>`
    );

    const textareaMatch = result.match(/<textarea[^>]*>[\s\S]*?<\/textarea>/);
    if (textareaMatch) {
        const textareaTag = textareaMatch[0].match(/<textarea[^>]*>/)[0];
        result = result.replace(
            /<textarea[^>]*>[\s\S]*?<\/textarea>/,
            textareaTag + editorContent + '</textarea>'
        );
    }

    if (nodePort !== 0) {
        const postData = result;
        const instanceBasename = path.basename(instancePath);
        const options = {
            hostname: 'localhost',
            port: nodePort,
            path: '/save',
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',
                'X-Filename': instanceBasename,
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    console.log(`  [OK] Node save triggered on port ${nodePort}`);
                } else {
                    const isSafety = body.includes('SAFETY ERROR');
                    console.error(`  [ERR] Node save (${res.statusCode}): ${isSafety ? 'SAFETY ERROR' : body}`);
                }
            });
        });
        req.on('error', (err) => {
            console.error(`  [ERR] Could not connect to port ${nodePort}: ${err.message}`);
        });
        req.write(postData);
        req.end();
    } else {
        fs.writeFileSync(instancePath, result, 'utf8');
        console.log(`  [OK] Saved to ${instancePath}`);
    }
}

main();
