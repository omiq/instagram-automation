""" Assumes the input WAV file is mono (1 channel) with 16 bit samples """

import sys

if len(sys.argv) != 2:
    print("Wrong number of arguments.")
    exit();

filename = sys.argv[1]

bytes = []
with open(filename, "br") as f:
    bytes = f.read()

# Parse according to format
# Here: http://soundfile.sapp.org/doc/WaveFormat/

chunkID = bytes[0:4].decode()
chunkSize = int.from_bytes(bytes[4:8], byteorder='little')
innerFormat = bytes[8:12].decode()
subchunk1ID = bytes[12:16].decode()
subchunk1Size = int.from_bytes(bytes[16:20], byteorder='little')
audioFormat = int.from_bytes(bytes[20:22], byteorder='little')
numChannels = int.from_bytes(bytes[22:24], byteorder='little')
sampleRate = int.from_bytes(bytes[24:28], byteorder='little')
byteRate = int.from_bytes(bytes[28:32], byteorder='little')
blockAlign = int.from_bytes(bytes[32:34], byteorder='little')
bitsPerSample = int.from_bytes(bytes[34:36], byteorder='little')
subchunk2ID = bytes[36:40].decode()
subchunk2Size = int.from_bytes(bytes[40:44], byteorder='little')

data = []
lastSample = 40 + subchunk2Size
for byte_pair in zip(bytes[40:lastSample:2], bytes[41:lastSample:2]):
    data.append((int.from_bytes(byte_pair, byteorder='little', signed=True)))

print('chunkID\t\t%s' % chunkID)
print('chunkSize\t%d' % chunkSize)
print('innerFormat\t%s' % innerFormat)
print('subchunk1ID\t%s' % subchunk1ID)
print('subchunk1Size\t%d' % subchunk1Size)
print('audioFormat\t%d' % audioFormat)
print('numChannels\t%d' % numChannels)
print('sampleRate\t%d' % sampleRate)
print('byteRate\t%d' % byteRate)
print('blockAlign\t%d' % blockAlign)
print('bitsPerSample\t%d' % bitsPerSample)
print('subchunk2ID\t%s' % subchunk2ID)
print('subchunk2Size\t%d' % subchunk2Size)

print("Actual size of data (16 bit words): %d" % len(data))

assert (chunkSize == 4 + (8 + subchunk1Size) + (8 + subchunk2Size))
assert (byteRate == sampleRate * numChannels * (bitsPerSample / 8))
assert (blockAlign == numChannels * (bitsPerSample / 8))
assert (subchunk2Size == len(data) * numChannels * (bitsPerSample / 8))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


with open('wav_data.h', 'w') as f:
    f.write(
        """
        #ifndef WAV_DATA
        #define WAV_DATA
        
        #define NUM_SAMPLES %d
        #define SAMPLE_RATE %d
        
        int16_t data[NUM_SAMPLES] PROGMEM = {
        
        """ % (len(data), sampleRate))

    for row in chunks(data, 8):
        f.write("    ");
        f.write(", ".join(list((str(word) for word in row))))
        f.write(",")
        f.write("\n")

    f.write("};\n")
    f.write("#endif\n\n")

try:
    import matplotlib.pylab as plt

    plt.plot(data)
    plt.show()
except:
    None