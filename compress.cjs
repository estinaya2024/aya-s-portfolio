const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');
const ffmpeg = require('@ffmpeg-installer/ffmpeg');

console.log('=============================================');
console.log('   Portfolio Video Compression Tool (Node)  ');
console.log('=============================================');
console.log('[+] Self-contained FFmpeg binary found at:');
console.log('   ', ffmpeg.path);

const videos = [
  'about-record.mp4',
  'boutique-record.mp4',
  'dashboard-record.mp4',
  'plat-record.mp4',
  'process-record.mp4',
  'region-record.mp4'
];

const publicDir = path.join(__dirname, 'public');

let index = 0;

function compressNext() {
  if (index >= videos.length) {
    console.log('\n[+] All videos successfully compressed! Your portfolio is now ultra-lightweight.');
    console.log('=============================================');
    return;
  }

  const video = videos[index];
  const inputPath = path.join(publicDir, video);
  const outputPath = path.join(publicDir, 'compressed_' + video);

  if (!fs.existsSync(inputPath)) {
    console.log(`[!] File not found: ${video}, skipping...`);
    index++;
    compressNext();
    return;
  }

  const originalSize = fs.statSync(inputPath).size / (1024 * 1024);
  console.log(`\n[*] Compressing ${video} (${originalSize.toFixed(2)} MB)...`);

  // ffmpeg arguments
  const args = [
    '-y',
    '-i', inputPath,
    '-vcodec', 'libx264',
    '-crf', '31',
    '-preset', 'faster',
    '-vf', 'scale=960:-2',
    '-an',
    outputPath
  ];

  execFile(ffmpeg.path, args, (err, stdout, stderr) => {
    if (err) {
      console.error(`[X] Failed to compress ${video}:`, err.message);
      index++;
      compressNext();
      return;
    }

    if (fs.existsSync(outputPath)) {
      const compressedSize = fs.statSync(outputPath).size / (1024 * 1024);
      const savingPercent = ((originalSize - compressedSize) / originalSize) * 100;

      // Replace original file with compressed one
      fs.unlinkSync(inputPath);
      fs.renameSync(outputPath, inputPath);

      console.log(`[+] Finished ${video}!`);
      console.log(`    New Size: ${compressedSize.toFixed(2)} MB`);
      console.log(`    Reduced by: ${savingPercent.toFixed(1)}%`);
    } else {
      console.error(`[X] Compressed file not found for ${video}`);
    }

    index++;
    compressNext();
  });
}

compressNext();
