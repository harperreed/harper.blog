// Constants
const API_BASE_URL = "https://public.api.bsky.app/xrpc";
const BSKY_WEB_URL = "https://bsky.app";
const RESOLVE_HANDLE_URL =
    "https://bsky.social/xrpc/com.atproto.identity.resolveHandle";

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
    const link = document.createElement("a");
    link.href = href;
    link.textContent = text;
    link.target = target;
    return link;
};

// API interaction class
class BlueskyAPI {
    static async resolveHandle(handle) {
        const url = `${RESOLVE_HANDLE_URL}?handle=${encodeURIComponent(handle)}`;
        const response = await fetch(url);

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
    }

    static async getPostThread(atUri) {
        const params = new URLSearchParams({ uri: atUri });
        const response = await fetch(
            `${API_BASE_URL}/app.bsky.feed.getPostThread?${params.toString()}`,
            {
                headers: { Accept: "application/json" },
                cache: "no-store",
            },
        );

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
    }
}

// Comment renderer class
class CommentRenderer {
    constructor(container) {
        this.container = container;
    }

    renderMetadata(thread) {
        const postUrl = this.createPostUrl(thread.post);

        const metaDiv = createElementWithClass("div", "bsky-meta");
        const stats = [
            `${thread.post.likeCount ?? 0} likes`,
            `${thread.post.repostCount ?? 0} reposts`,
            `${thread.post.replyCount ?? 0} replies on bluesky`,
        ].join(" | ");

        metaDiv.appendChild(createLink(postUrl, stats));

        return metaDiv;
    }

    renderComment(comment) {
        if (!this.isValidComment(comment)) {
            console.warn("Invalid comment data:", comment);
            return null;
        }

        const { post, replies } = comment;
        const commentDiv = createElementWithClass("div", "bsky-comment");

        // Author section
        commentDiv.appendChild(this.renderAuthor(post.author));

        // Content section
        const content = createElementWithClass("p", "bsky-content");
        content.textContent = post.record.text;
        commentDiv.appendChild(content);

        // Actions section
        commentDiv.appendChild(this.renderActions(post));

        // Nested replies
        if (replies?.length > 0) {
            const nestedReplies = createElementWithClass(
                "div",
                "bsky-nested-replies",
            );
            replies
                .sort(this.sortByLikes.bind(this))
                .filter((reply) => this.isValidComment(reply))
                .forEach((reply) => {
                    const renderedReply = this.renderComment(reply);
                    if (renderedReply) nestedReplies.appendChild(renderedReply);
                });
            commentDiv.appendChild(nestedReplies);
        }

        return commentDiv;
    }

    renderAuthor(author) {
        const authorDiv = createElementWithClass("div", "bsky-author");

        if (author.avatar) {
            const avatar = document.createElement("img");
            avatar.src = author.avatar;
            avatar.alt = `${author.handle}'s avatar`;
            avatar.className = "bsky-avatar img loaded";
            avatar.loading = "lazy";
            authorDiv.appendChild(avatar);
        }

        const authorLink = createLink(
            `${BSKY_WEB_URL}/profile/${author.did}`,
            author.displayName ?? author.handle,
        );
        authorDiv.appendChild(authorLink);

        const handle = document.createElement("span");
        handle.className = "bsky-handle";
        handle.textContent = `@${author.handle}`;
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

    createPostUrl(post) {
        return `${BSKY_WEB_URL}/profile/${post.author.did}/post/${post.uri.split("/").pop()}`;
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
    constructor(container) {
        this.container = container;
        this.renderer = new CommentRenderer(container);
    }

    async initialize() {
        const bskyWebUrl = this.container.getAttribute("data-bsky-uri");
        if (!bskyWebUrl) {
            throw new ValidationError("Missing data-bsky-uri attribute");
        }

        try {
            const atUri = await this.extractAtUri(bskyWebUrl);
            const thread = await BlueskyAPI.getPostThread(atUri);
            await this.render(thread);
        } catch (error) {
            this.handleError(error);
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
        this.container.innerHTML = "";

        // Add metadata
        this.container.appendChild(document.createElement("hr"));
        this.container.appendChild(this.renderer.renderMetadata(thread));

        // Add header
        const header = document.createElement("h2");
        header.textContent = "Comments";
        this.container.appendChild(header);

        // Add reply link
        const replySection = document.createElement("p");
        replySection.textContent = "Reply on Bluesky ";
        replySection.appendChild(
            createLink(this.createPostUrl(thread.post), "here"),
        );
        this.container.appendChild(replySection);

        this.container.appendChild(document.createElement("hr"));

        // Render comments
        if (thread.replies?.length > 0) {
            const commentsContainer = createElementWithClass(
                "div",
                "bsky-comments-container",
            );
            thread.replies
                .sort(this.renderer.sortByLikes.bind(this.renderer))
                .filter((reply) => this.renderer.isValidComment(reply))
                .forEach((reply) => {
                    const renderedComment = this.renderer.renderComment(reply);
                    if (renderedComment)
                        commentsContainer.appendChild(renderedComment);
                });
            this.container.appendChild(commentsContainer);
        } else {
            const noComments = document.createElement("p");
            noComments.textContent = "No comments available.";
            this.container.appendChild(noComments);
        }

        this.container.appendChild(document.createElement("hr"));
    }

    createPostUrl(post) {
        return `${BSKY_WEB_URL}/profile/${post.author.did}/post/${post.uri.split("/").pop()}`;
    }

    handleError(error) {
        console.error("BlueskyCommentsWidget Error:", error);
        this.container.textContent =
            error instanceof ValidationError
                ? `Configuration error: ${error.message}`
                : "Error loading comments.";
    }
}

// Initialize widget
document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("comments-section");
    if (container) {
        const widget = new BlueskyCommentsWidget(container);
        widget.initialize().catch((error) => {
            console.error("Failed to initialize BlueskyCommentsWidget:", error);
        });
    }
});
