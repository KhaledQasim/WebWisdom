import React from 'react';
import DOMPurify from 'dompurify';

function HtmlContent({ html }) {
    // Sanitize the HTML before setting it
    const safeHtml = DOMPurify.sanitize(html);

    return (
        <div dangerouslySetInnerHTML={{ __html: safeHtml }} />
    );
}

export default HtmlContent;
