// Constants
const API_BASE_URL = "https://public.api.bsky.app/xrpc";
const BSKY_WEB_URL = "https://bsky.app";
const RESOLVE_HANDLE_URL =
    "https://bsky.social/xrpc/com.atproto.identity.resolveHandle";

// Configuration
const CONFIG = {
    TIMEOUTS: {
        API_REQUEST: 10000, // 10 seconds
        IMAGE_LOAD: 5000    // 5 seconds
    },
    LIMITS: {
        MAX_NESTED_DEPTH: 3,
        MAX_COMMENTS_PER_LEVEL: 50
    },
    UI: {
        ENABLE_AVATARS: true,
        SORT_BY: 'likes', // 'likes' | 'date'
        SHOW_LOADING: true
    }
};

// Types and validation
class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}

// Utility functions
const createElementWithClass = (tag, className) => {
    const element = document.createElement(tag);
    if (className) element.className = className;
    return element;
};

const createLink = (href, text, target = "_blank") => {
    // Security: Validate URL protocol to prevent XSS
    if (href.startsWith('javascript:') || href.startsWith('data:') || href.startsWith('vbscript:')) {
        throw new ValidationError('Invalid URL protocol detected');
    }
    
    const link = document.createElement("a");
    link.href = href;
    link.textContent = text;
    link.target = target;
    link.rel = "noopener noreferrer"; // Security: Prevent window.opener access
    return link;
};

// API interaction class
class BlueskyAPI {
    static async resolveHandle(handle) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.TIMEOUTS.API_REQUEST);
        
        try {
            const url = `${RESOLVE_HANDLE_URL}?handle=${encodeURIComponent(handle)}`;
            const response = await fetch(url, {
                signal: controller.signal,
                headers: { Accept: "application/json" }
            });
            
            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new ValidationError(
                    `Failed to resolve handle: ${await response.text()}`,
                );
            }

            const data = await response.json();
            if (!data.did) {
                throw new ValidationError("DID not found in response");
            }

            return data.did;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Request timeout: Failed to resolve handle');
            }
            throw error;
        }
    }

    static async getPostThread(atUri) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.TIMEOUTS.API_REQUEST);
        
        try {
            const params = new URLSearchParams({ uri: atUri });
            const response = await fetch(
                `${API_BASE_URL}/app.bsky.feed.getPostThread?${params.toString()}`,
                {
                    headers: { Accept: "application/json" },
                    cache: "no-store",
                    signal: controller.signal
                },
            );
            
            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(
                    `Failed to fetch post thread: ${await response.text()}`,
                );
            }

            const data = await response.json();
            if (
                !data.thread ||
                data.thread.$type !== "app.bsky.feed.defs#threadViewPost"
            ) {
                throw new ValidationError("Invalid thread data received");
            }

            return data.thread;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Request timeout: Failed to fetch post thread');
            }
            throw error;
        }
    }
}

// Utility function for creating post URLs (fixes duplicate code)
const createPostUrl = (post) => {
    return `${BSKY_WEB_URL}/profile/${post.author.did}/post/${post.uri.split("/").pop()}`;
};

// Comment renderer class
class CommentRenderer {
    constructor(container) {
        this.container = container;
    }

    renderMetadata(thread) {
        const postUrl = createPostUrl(thread.post);

        const metaDiv = createElementWithClass("div", "bsky-meta");
        const stats = [
            `${thread.post.likeCount ?? 0} likes`,
            `${thread.post.repostCount ?? 0} reposts`,
            `${thread.post.replyCount ?? 0} replies on bluesky`,
        ].join(" | ");

        metaDiv.appendChild(createLink(postUrl, stats));

        return metaDiv;
    }

    renderComment(comment, depth = 0) {
        if (!this.isValidComment(comment)) {
            console.warn("Invalid comment data:", comment);
            return null;
        }

        const { post, replies } = comment;
        // Use semantic HTML for better accessibility
        const commentDiv = createElementWithClass("article", "bsky-comment");
        commentDiv.setAttribute('role', 'comment');
        commentDiv.setAttribute('aria-label', `Comment by ${post.author.displayName || post.author.handle}`);

        // Author section
        commentDiv.appendChild(this.renderAuthor(post.author));

        // Content section
        const content = createElementWithClass("p", "bsky-content");
        content.textContent = post.record.text;
        content.setAttribute('aria-label', 'Comment content');
        commentDiv.appendChild(content);

        // Actions section
        commentDiv.appendChild(this.renderActions(post));

        // Nested replies (limit depth to prevent infinite nesting)
        if (replies?.length > 0 && depth < CONFIG.LIMITS.MAX_NESTED_DEPTH) {
            const nestedReplies = createElementWithClass(
                "div",
                "bsky-nested-replies",
            );
            nestedReplies.setAttribute('role', 'group');
            nestedReplies.setAttribute('aria-label', 'Nested replies');
            
            const limitedReplies = replies
                .sort(this.sortByLikes.bind(this))
                .filter((reply) => this.isValidComment(reply))
                .slice(0, CONFIG.LIMITS.MAX_COMMENTS_PER_LEVEL);
                
            limitedReplies.forEach((reply) => {
                const renderedReply = this.renderComment(reply, depth + 1);
                if (renderedReply) nestedReplies.appendChild(renderedReply);
            });
            
            if (limitedReplies.length > 0) {
                commentDiv.appendChild(nestedReplies);
            }
        }

        return commentDiv;
    }

    renderAuthor(author) {
        // Use semantic HTML header element
        const authorDiv = createElementWithClass("header", "bsky-author");
        authorDiv.setAttribute('role', 'banner');
        authorDiv.setAttribute('aria-label', `Author: ${author.displayName || author.handle}`);

        if (author.avatar && CONFIG.UI.ENABLE_AVATARS) {
            const avatar = document.createElement("img");
            avatar.src = author.avatar;
            avatar.alt = `${author.displayName || author.handle}'s avatar`;
            avatar.className = "bsky-avatar img loaded";
            avatar.loading = "lazy";
            
            // Add error handling for avatar images
            avatar.onerror = () => {
                avatar.style.display = 'none';
                console.warn('Failed to load avatar for', author.handle);
            };
            
            // Add timeout for slow-loading images
            const timeoutId = setTimeout(() => {
                if (!avatar.complete) {
                    avatar.style.display = 'none';
                    console.warn('Avatar loading timeout for', author.handle);
                }
            }, CONFIG.TIMEOUTS.IMAGE_LOAD);
            
            avatar.onload = () => {
                clearTimeout(timeoutId);
            };
            
            authorDiv.appendChild(avatar);
        }

        const authorLink = createLink(
            `${BSKY_WEB_URL}/profile/${author.did}`,
            author.displayName ?? author.handle,
        );
        authorLink.setAttribute('aria-label', `View ${author.displayName || author.handle}'s profile`);
        authorDiv.appendChild(authorLink);

        const handle = document.createElement("span");
        handle.className = "bsky-handle";
        handle.textContent = `@${author.handle}`;
        handle.setAttribute('aria-label', `Username: ${author.handle}`);
        authorDiv.appendChild(handle);

        return authorDiv;
    }

    renderActions(post) {
        const actions = createElementWithClass("div", "bsky-actions");
        actions.textContent = [
            `${post.replyCount ?? 0} replies`,
            `${post.repostCount ?? 0} reposts`,
            `${post.likeCount ?? 0} likes`,
        ].join(" | ");
        return actions;
    }

    isValidComment(obj) {
        return obj && obj.$type === "app.bsky.feed.defs#threadViewPost";
    }

    sortByLikes(a, b) {
        if (!a?.post?.likeCount || !b?.post?.likeCount) return 0;
        return b.post.likeCount - a.post.likeCount;
    }
}

// Main widget class
class BlueskyCommentsWidget {
    constructor(container, options = {}) {
        this.container = container;
        this.renderer = new CommentRenderer(container);
        this.options = {
            maxDepth: CONFIG.LIMITS.MAX_NESTED_DEPTH,
            timeout: CONFIG.TIMEOUTS.API_REQUEST,
            showAvatars: CONFIG.UI.ENABLE_AVATARS,
            sortBy: CONFIG.UI.SORT_BY,
            showLoading: CONFIG.UI.SHOW_LOADING,
            ...options
        };
        this.state = {
            loading: false,
            error: null,
            thread: null
        };
    }

    async initialize() {
        const bskyWebUrl = this.container.getAttribute("data-bsky-uri");
        if (!bskyWebUrl) {
            throw new ValidationError("Missing data-bsky-uri attribute");
        }

        try {
            this.setState({ loading: true, error: null });
            if (this.options.showLoading) {
                this.showLoading();
            }
            
            const atUri = await this.extractAtUri(bskyWebUrl);
            const thread = await BlueskyAPI.getPostThread(atUri);
            
            this.setState({ thread, loading: false });
            await this.render(thread);
        } catch (error) {
            this.setState({ loading: false, error });
            this.handleError(error);
        }
    }
    
    setState(newState) {
        this.state = { ...this.state, ...newState };
    }
    
    showLoading() {
        this.container.innerHTML = '<div class="bsky-loading" role="status" aria-live="polite">Loading comments...</div>';
    }
    
    hideLoading() {
        const loadingElement = this.container.querySelector('.bsky-loading');
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    async extractAtUri(webUrl) {
        const url = new URL(webUrl);
        const pathSegments = url.pathname.split("/").filter(Boolean);

        if (
            pathSegments.length < 4 ||
            pathSegments[0] !== "profile" ||
            pathSegments[2] !== "post"
        ) {
            throw new ValidationError("Invalid URL format");
        }

        const handleOrDid = pathSegments[1];
        const postID = pathSegments[3];
        const did = handleOrDid.startsWith("did:")
            ? handleOrDid
            : await BlueskyAPI.resolveHandle(handleOrDid);

        return `at://${did}/app.bsky.feed.post/${postID}`;
    }

    async render(thread) {
        this.hideLoading();
        this.container.innerHTML = "";

        // Add metadata
        this.container.appendChild(document.createElement("hr"));
        this.container.appendChild(this.renderer.renderMetadata(thread));

        // Add header with proper semantic HTML
        const header = document.createElement("h2");
        header.textContent = "Comments";
        header.setAttribute('id', 'comments-heading');
        this.container.appendChild(header);

        // Add reply link
        const replySection = document.createElement("p");
        replySection.textContent = "Reply on Bluesky ";
        replySection.appendChild(
            createLink(createPostUrl(thread.post), "here"),
        );
        this.container.appendChild(replySection);

        this.container.appendChild(document.createElement("hr"));

        // Render comments with improved structure
        if (thread.replies?.length > 0) {
            const commentsContainer = createElementWithClass(
                "section",
                "bsky-comments-container",
            );
            commentsContainer.setAttribute('aria-labelledby', 'comments-heading');
            commentsContainer.setAttribute('role', 'main');
            
            const sortedReplies = thread.replies
                .sort(this.renderer.sortByLikes.bind(this.renderer))
                .filter((reply) => this.renderer.isValidComment(reply))
                .slice(0, CONFIG.LIMITS.MAX_COMMENTS_PER_LEVEL);
                
            sortedReplies.forEach((reply) => {
                const renderedComment = this.renderer.renderComment(reply, 0);
                if (renderedComment)
                    commentsContainer.appendChild(renderedComment);
            });
            
            this.container.appendChild(commentsContainer);
            
            // Show count of loaded comments
            if (sortedReplies.length > 0) {
                const countInfo = document.createElement("p");
                countInfo.className = "bsky-comment-count";
                countInfo.textContent = `Showing ${sortedReplies.length} of ${thread.replies.length} comments`;
                countInfo.setAttribute('aria-live', 'polite');
                this.container.appendChild(countInfo);
            }
        } else {
            const noComments = document.createElement("p");
            noComments.textContent = "No comments available.";
            noComments.setAttribute('role', 'status');
            noComments.setAttribute('aria-live', 'polite');
            this.container.appendChild(noComments);
        }

        this.container.appendChild(document.createElement("hr"));
    }


    handleError(error) {
        console.error("BlueskyCommentsWidget Error:", error);
        this.hideLoading();
        
        const errorDiv = createElementWithClass("div", "bsky-error");
        errorDiv.setAttribute('role', 'alert');
        errorDiv.setAttribute('aria-live', 'assertive');
        
        const errorMessage = error instanceof ValidationError
            ? `Configuration error: ${error.message}`
            : error.message.includes('timeout')
            ? "Request timed out. Please try again later."
            : "Error loading comments. Please try again later.";
            
        errorDiv.textContent = errorMessage;
        
        // Add retry button for non-configuration errors
        if (!(error instanceof ValidationError)) {
            const retryButton = document.createElement("button");
            retryButton.textContent = "Retry";
            retryButton.className = "bsky-retry-button";
            retryButton.setAttribute('aria-label', 'Retry loading comments');
            retryButton.onclick = () => {
                this.initialize().catch(err => console.error('Retry failed:', err));
            };
            errorDiv.appendChild(document.createElement("br"));
            errorDiv.appendChild(retryButton);
        }
        
        this.container.innerHTML = "";
        this.container.appendChild(errorDiv);
    }
}

// Debounced initialization to prevent multiple rapid calls
let initializationTimeout;
const debounceInitialization = (callback, delay = 100) => {
    clearTimeout(initializationTimeout);
    initializationTimeout = setTimeout(callback, delay);
};

// Initialize widget with debouncing
document.addEventListener("DOMContentLoaded", () => {
    debounceInitialization(() => {
        const container = document.getElementById("comments-section");
        if (container && !container.dataset.bskyInitialized) {
            // Mark as initialized to prevent duplicate initialization
            container.dataset.bskyInitialized = "true";
            
            const widget = new BlueskyCommentsWidget(container);
            widget.initialize().catch((error) => {
                console.error("Failed to initialize BlueskyCommentsWidget:", error);
                // Remove initialization flag on error to allow retry
                delete container.dataset.bskyInitialized;
            });
        }
    });
});

// Export for manual initialization if needed
if (typeof window !== 'undefined') {
    window.BlueskyCommentsWidget = BlueskyCommentsWidget;
}
