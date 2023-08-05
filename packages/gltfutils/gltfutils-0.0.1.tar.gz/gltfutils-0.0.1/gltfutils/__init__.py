from dataclasses import dataclass, field, fields, MISSING, is_dataclass, replace
from typing import *
from enum import IntEnum, Enum
import json
import hashlib
from struct import Struct
import os
import itertools

from datauri import *


GLB_MAGIC = 0x46546C67


@dataclass
class vec2:
    x: float = 0.0
    y: float = 0.0

    def to_bytes(self):
        return struct.pack("ff", self.x, self.y)

    def __iter__(self):
        yield from [self.x, self.y]

    def swizzle(self, s):
        lut = {
            'x': self.x,
            'y': self.y,
            '0': 0.0,
            '1': 1.0
        }
        # TODO: return the correct type given the size of s.
        return [lut[c] for c in s]


@dataclass
class vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_bytes(self):
        return struct.pack("fff", self.x, self.y, self.z)

    def __iter__(self):
        yield from [self.x, self.y, self.z]

    def swizzle(self, s):
        lut = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            '0': 0.0,
            '1': 1.0
        }
        return [lut[c] for c in s]
    


@dataclass
class vec4:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0

    def to_bytes(self):
        return struct.pack("ffff", self.x, self.y, self.z, self.w)

    def __iter__(self):
        yield from [self.x, self.y, self.z, self.w]

    def swizzle(self, s):
        lut = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'w': self.w,
            '0': 0.0,
            '1': 1.0
        }
        return [lut[c] for c in s]


@dataclass
class mat2:
    c0: vec2 = field(default_factory=lambda: vec2(1.0, 0.0))
    c1: vec2 = field(default_factory=lambda: vec2(0.0, 1.0))
    struct: ClassVar[Struct] =Struct('f'*4)

    def elements(self):
        for c in self:
            yield from c

    def to_bytes(self):
        return self.struct.pack(*self.elements())

    def __iter__(self):
        yield self.c0
        yield self.c1

    def __getitem__(self, i):
        return [self.c0, self.c1][i]

    def __len__(self):
        return 2


@dataclass
class mat3:
    c0: vec3 = field(default_factory=lambda: vec3(1.0, 0.0, 0.0))
    c1: vec3 = field(default_factory=lambda: vec3(0.0, 1.0, 0.0))
    c2: vec3 = field(default_factory=lambda: vec3(0.0, 0.0, 1.0))
    struct: ClassVar[Struct] = Struct('f'*9)

    def elements(self):
        for c in self:
            yield from c

    def to_bytes(self):
        return self.struct.pack(self.elements())

    def __iter__(self):
        yield self.c0
        yield self.c1
        yield self.c2

    def __getitem__(self, i):
        return [self.c0, self.c1, self.c2][i]

    def __len__(self):
        return 3


@dataclass
class mat4:
    c0: vec4 = field(default_factory=lambda: vec4(1.0, 0.0, 0.0, 0.0))
    c1: vec4 = field(default_factory=lambda: vec4(0.0, 1.0, 0.0, 0.0))
    c2: vec4 = field(default_factory=lambda: vec4(0.0, 0.0, 1.0, 0.0))
    c3: vec4 = field(default_factory=lambda: vec4(0.0, 0.0, 0.0, 1.0))
    struct: ClassVar[Struct] = Struct('f'*16)

    def elements(self):
        for c in self:
            yield from c

    def to_bytes(self):
        return self.struct.pack(*self.elements())

    def __iter__(self):
        yield self.c0
        yield self.c1
        yield self.c2
        yield self.c3

    def __getitem__(self, i):
        return [self.c0, self.c1, self.c2, self.c3][i]

    def __len__(self):
        return 4


def hash_json(data: Any) -> str:
    s = json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    return hashlib.md5(s).hexdigest() 


def to_json(element: Any) -> Any:
    result = {}

    for field in fields(element):
        value = getattr(element, field.name)
        original_value = value

        # this is only really used for Asset right now,
        # though in the future it will be used for pbr parts of material.
        # convert more complex types like containers of objects
        if field.type in TYPE_TO_JSON:
            value = TYPE_TO_JSON[field.type](value)

        required = field.metadata.get('required', False)
        serialize = field.metadata.get('serialize', True)
        has_default = field.default is not MISSING
        has_factory = field.default_factory is not MISSING

        # don't bother putting the default value in JSON.
        if (not required) and ((has_default and value == field.default) or (has_factory and value == field.default_factory())):
            continue

        if serialize:
            result[field.name] = value

    return result


def convert_list(element_converter):
    def func(data):
        return [element_converter(e) for e in data]
    return func


def convert_optional(element_converter):
    def func(data):
        return element_converter(data) if data is not None else None
    return func


def from_json(cls, data):
    args = {}
    for field in fields(cls):
        value = None

        if field.name in data:
            value = data[field.name]
            if field.type in TYPE_FROM_JSON:
                value = TYPE_FROM_JSON[field.type](value)
        elif field.metadata.get('required', False):
            raise ValueError(f'required field missing: "{field.name}"')
        elif field.default != MISSING:
            value = field.default
        else:
            value = field.default_factory()
        
        args[field.name] = value

    return cls(**args)


Extras = Optional[Any]
Extensions = Optional[Dict[str,Any]]


@dataclass
class Element:
    extensions: Extensions = None
    extras: Extras = None

    @classmethod
    def from_json(cls, data):
        return from_json(cls, data)


@dataclass
class Asset(Element):
    version: str = field(default="2.0", metadata={'required':True})
    generator: Optional[str] = None
    minVersion: Optional[str] = None
    copyright: Optional[str] = None


@dataclass
class Scene(Element):
    # the scenes here must be root nodes; i.e. they must not have parents
    nodes: List[int] = field(default_factory=list)
    name: Optional[str] = None


Mat4 = Tuple[
    float, float, float, float,
    float, float, float, float,
    float, float, float, float,
    float, float, float, float
]

DEFAULT_MATRIX = (
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 1.0
)

Quat = Tuple[float, float, float, float]
DEFAULT_ROTATION = (0.0, 0.0, 0.0, 1.0)

Vec3 = Tuple[float, float, float]
DEFAULT_SCALE = (1.0, 1.0, 1.0)
DEFAULT_TRANSLATION = (0.0, 0.0, 0.0)


@dataclass
class Node(Element):
    name: Optional[str] = None
    camera: Optional[int] = None
    children: Optional[List[int]] = field(default_factory=list)
    skin: Optional[int] = None
    mesh: Optional[int] = None
    weights: Optional[List[float]] = None
        
    # If the determinant of the transform is a negative value, the winding 
    # order of the mesh triangle faces should be reversed. This supports negative 
    # scales for mirroring geometry.
    matrix: Optional[Mat4] = DEFAULT_MATRIX
    rotation: Optional[Quat] = DEFAULT_ROTATION
    scale: Optional[Vec3] = DEFAULT_SCALE
    translation: Optional[Vec3] = DEFAULT_TRANSLATION



@dataclass
class Primitive(Element):
    attributes:Dict[str,int] = field(default_factory=dict)
    indices: Optional[int] = None
    material: Optional[int] = None
    mode: Optional[int] = None
    targets: Optional[Dict[str,int]] = field(default_factory=dict)


@dataclass
class Mesh(Element):
    name: Optional[str] = None
    primitives: Optional[List[Primitive]] = field(default_factory=list)
    weights: Optional[List[float]] = field(default_factory=list)


@dataclass
class Buffer(Element):
    uri: Optional[str] = None
    byteLength: int = field(default=0, metadata={'required': True})
    name: Optional[str] = None
    data: Optional[bytearray] = field(default=None, metadata={'serialize':False})

    def load_from_file(self, base_path=None):
        path = self.uri
        if base_path is not None:
            path = os.path.join(base_path, path)
        with open(path, 'rb') as f:
            self.data = f.read()

    def load_from_data_uri(self):
        uri = DataURI(self.uri)
        self.data = uri.data

    def load_from_glb(self, glb):
        assert(glb.chunks[1].chunkType == ChunkType.BIN)
        self.data = glb.chunks[1].chunkData

    def load(self, glb=None, base_path=None):
        if self.uri is None:
            self.load_from_glb(glb)
        elif self.uri.startswith('data:'):
            self.load_from_data_uri()
        else:
            self.load_from_file(base_path)

        # raise ValueError('uri might be valid, dunno.')


@dataclass
class BufferView(Element):
    # When a buffer view contain vertex indices or attributes,
    # they must be its only content, i.e., it's invalid to have 
    # more than one kind of data in the same buffer view.
    name: Optional[str] = None
    buffer: Optional[int] = None
    byteLength: Optional[int] = None
    byteOffset: Optional[int] = None
    # When a buffer view is used for vertex attribute data, it
    # may have a byteStride property. This property defines the
    # stride in bytes between each vertex.
    byteStride: Optional[int] = None
    target: Optional[int] = None



class ComponentType(IntEnum):
    BYTE = 5120
    UNSIGNED_BYTE = 5121
    SHORT = 5122
    UNSIGNED_SHORT = 5123
    UNSIGNED_INT = 5125
    FLOAT = 5126

    def byte_size(self):
        return {
            self.BYTE: 1,
            self.UNSIGNED_BYTE: 1,
            self.SHORT: 2,
            self.UNSIGNED_SHORT: 2,
            self.UNSIGNED_INT: 4,
            self.FLOAT: 4
        }[self]

    def struct_format(self):
        return {
            self.BYTE: "b",
            self.UNSIGNED_BYTE: "B",
            self.SHORT: "h",
            self.UNSIGNED_SHORT: "H",
            self.UNSIGNED_INT: "I",
            self.FLOAT: "f"
        }[self]



@dataclass
class SparseIndices(Element):
    bufferView: int = field(default=0, metadata={'required':True})
    byteOffset: int = 0
    componentType: ComponentType = field(default=ComponentType.FLOAT, metadata={'required':True})


@dataclass
class SparseValues(Element):
    bufferView: int = field(default=0, metadata={'required':True})
    byteOffset: int = 0


@dataclass
class Sparse(Element):
    count: int = field(default=0, metadata={'required':True})
    indices: SparseIndices = field(default_factory=SparseIndices, metadata={'required':True})
    values: SparseValues = field(default_factory=SparseValues, metadata={'required':True})


def component_count_from_type(t):
    return {
        "SCALAR": 1,
        "VEC2": 2,
        "VEC3": 3,
        "VEC4": 4
    }[t]


@dataclass
class Accessor(Element):
    bufferView: Optional[int] = None
    byteOffset: Optional[int] = 0
    componentType: ComponentType = field(default=ComponentType.FLOAT, metadata={'required':True})
    normalized: bool = False
    count: int = field(default=0, metadata={'required': True})
    type: str = field(default="SCALAR", metadata={'required': True})
    max: Optional[List[float]] = None
    min: Optional[List[float]] = None
    sparse: Optional[Sparse] = None
    name: Optional[str] = None

    def component_count(self):
        return component_count_from_type(self.type)

    def component_byte_size(self):
        return self.componentType.byte_size()

    def element_byte_size(self):
        return self.component_count() * self.component_byte_size()

    def struct_format_str(self):
        return self.componentType.struct_format() * self.component_count()


@dataclass
class TextureInfo(Element):
    index: Optional[int] = None
    texCoord: Optional[int] = 0


@dataclass
class NormalTextureInfo(TextureInfo):
    scale: Optional[float] = 1.0


@dataclass
class OcclusionTextureInfo(TextureInfo):
    strength: Optional[float] = 1.0


@dataclass
class PBRMetallicRoughness(Element):
    baseColorFactor: Optional[Tuple[float, float, float]] = None
    baseColorTexture: Optional[TextureInfo] = None
    metallicFactor: Optional[float] = None
    metallicRoughnessTexture: Optional[int] = None
    roughnessFactor: Optional[float] = None


@dataclass
class Material(Element):
    name: Optional[str] = None
    pbrMetallicRoughness: Optional[PBRMetallicRoughness] = None
    normalTexture: Optional[NormalTextureInfo] = None
    emissiveTexture: Optional[TextureInfo] = None
    occlusionTexture: Optional[OcclusionTextureInfo] = None
    emissiveFactor: Optional[Tuple[float, float, float]] = (0.0, 0.0, 0.0)
    doubleSided: Optional[bool] = None
    alphaMode: Optional[str] = None
    alphaCutoff: Optional[str] = None



@dataclass
class Perspective(Element):
    znear: Optional[float] = None
    zfar: Optional[float] = None
    yfov: Optional[float] = None
    aspectRatio: Optional[float] = None


@dataclass
class Camera(Element):
    name: Optional[str] = None
    type: Optional[str] = None
    perspective: Optional[Perspective] = None


@dataclass
class Image(Element):
    name: Optional[str] = None
    uri: Optional[str] = None
    mimeType: Optional[str] = None
    bufferView: Optional[int] = None


@dataclass
class Sampler(Element):
    name: Optional[str] = None
    input: Optional[int] = None
    minFilter: Optional[int] = None
    magFilter: Optional[int] = None
    wrapT: Optional[int] = None
    wrapS: Optional[int] = None


@dataclass
class Texture(Element):
    name: Optional[str] = None
    source: Optional[int] = None
    sampler: Optional[int] = None


@dataclass
class AnimationSampler(Element):
    input: Optional[int] = None
    interpolation: Optional[str] = None
    output: Optional[int] = None


@dataclass
class AnimationTarget(Element):
    node: Optional[int] = None
    path: Optional[str] = None


@dataclass
class AnimationChannel(Element):
    sampler: Optional[int] = None
    target: Optional[AnimationTarget] = None


@dataclass
class Animation(Element):
    name: Optional[str] = None
    channels: Optional[List[AnimationChannel]] = field(default_factory=list)
    samplers: Optional[List[AnimationSampler]] = field(default_factory=list)


@dataclass
class Skin(Element):
    name: Optional[str] = None
    inverseBindMatrices: Optional[int] = None
    skeleton: Optional[int] = None
    joints: Optional[List[int]] = None


data_types: List[Type[Element]] = [
    Asset,
    Node,
    Scene,
    Camera,
    Perspective,
    Material,
    PBRMetallicRoughness,
    Mesh,
    Buffer,
    BufferView,
    Accessor, 
    Image,
    Sampler,
    Texture,
    Animation,
    AnimationTarget,
    AnimationChannel,
    AnimationSampler,
    Skin,
    Material,
    TextureInfo,
    NormalTextureInfo,
    OcclusionTextureInfo,
    Primitive
]

TYPE_FROM_JSON = {Optional[List[t]]:convert_list(t.from_json) for t in data_types}
TYPE_FROM_JSON.update({Optional[t]:convert_optional(t.from_json) for t in data_types})
TYPE_FROM_JSON.update({t:t.from_json for t in data_types})


TYPE_TO_JSON = {Optional[List[t]]: convert_list(to_json) for t in data_types}
TYPE_TO_JSON.update({Optional[t]:convert_optional(to_json) for t in data_types})
TYPE_TO_JSON.update({t:to_json for t in data_types})


@dataclass
class GLTF2(Element):
    asset: Asset = field(default_factory=Asset, metadata={'required':True})
    scenes: Optional[List[Scene]] = field(default_factory=list)
    scene: Optional[int] = None
    nodes: Optional[List[Node]] = field(default_factory=list)
    meshes: Optional[List[Mesh]] = field(default_factory=list)
    buffers: Optional[List[Buffer]] = field(default_factory=list)
    bufferViews: Optional[List[BufferView]] = field(default_factory=list)
    accessors: Optional[List[Accessor]] = field(default_factory=list)
    materials: Optional[List[Material]] = field(default_factory=list)
    cameras: Optional[List[Camera]] = field(default_factory=list)
    images: Optional[List[Image]] = field(default_factory=list)
    samplers: Optional[List[Sampler]] = field(default_factory=list)
    textures: Optional[List[Texture]] = field(default_factory=list)
    animations: Optional[List[Animation]] = field(default_factory=list)
    skins: Optional[List[Skin]] = field(default_factory=list)
    extensionsUsed: Optional[List[str]] = None
    extensionsRequired: Optional[List[str]] = None

    def accessor_element(accessor_index:int, element_index:int):
        """
        It's probably best to design around generators rather than doing all this work each component access.
        """
        accessor = self.accessors[accessor_index]
        buffer_view = self.bufferViews[accessor.bufferView]
        buffer = self.buffers[buffer_view.buffer]
        size = accessor.element_byte_size()
        offset = buffer_view.byteOffset + buffer_view.byteStride * element_index + accessor.byteOffset
        return buffer.data[offset:offset+size]

    def accessor_elements(accessor_index:int):
        accessor = self.accessors[accessor_index]
        buffer_view = self.bufferViews[accessor.bufferView]
        buffer = self.buffers[buffer_view.buffer]
        size = accessor.element_byte_size()
        for i in range(buffer_view.count):
            offset = buffer_view.byteOffset + buffer_view.byteStride * i + accessor.byteOffset
            yield buffer.data[offset:offset+size]

    @classmethod
    def load(cls, f):
        return cls.from_json(json.load(f))

    def load_buffers(self, glb=None, base_path=None):
        for b in self.buffers:
            b.load(glb, base_path)


@dataclass
class GLBHeader:
    FORMAT: ClassVar[Struct] = Struct('<III')
    magic: int
    version: int
    length: int


@dataclass
class GLBChunk:
    FORMAT: ClassVar[Struct] = Struct('<II')
    chunkLength: int
    chunkType: int
    chunkData: bytes
    chunkJSON: Optional[GLTF2] = None


class ChunkType(IntEnum):
    BIN = 0x004E4942
    JSON = 0x4E4F534A


@dataclass
class GLB:
    header: GLBHeader
    chunks: List['GLB']

    @classmethod
    def load(cls, f, base_path=None):
        data = f.read(GLBHeader.FORMAT.size)
        header = GLBHeader(*GLBHeader.FORMAT.unpack(data))
        # TODO: validate magic
        chunk_header_data = f.read(GLBChunk.FORMAT.size)

        chunk = GLBChunk(*GLBChunk.FORMAT.unpack(chunk_header_data), None)
        chunk.chunkData = f.read(chunk.chunkLength)
        chunks = [chunk]

        if chunk.chunkType == ChunkType.JSON:
            s = chunk.chunkData.decode('utf-8')
            j = json.loads(s)
            chunk.chunkJSON = GLTF2.from_json(j)

        while f:
            chunk_header_data = f.read(GLBChunk.FORMAT.size)
            if not chunk_header_data:
                break
            chunk = GLBChunk(*GLBChunk.FORMAT.unpack(chunk_header_data), None)
            chunk.chunkData = f.read(chunk.chunkLength)
            chunks.append(chunk)

        return cls(header, chunks)
