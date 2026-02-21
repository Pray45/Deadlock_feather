/** @type {import('next').NextConfig} */
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const nextConfig = {
	// Explicitly set turbopack.root to avoid Next.js inferring the workspace root
	// when multiple lockfiles are present on the system.
	turbopack: {
		root: resolve(__dirname)
	}
};

export default nextConfig;
