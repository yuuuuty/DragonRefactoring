'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p
from OpenGL.GL import glget
EXTENSION_NAME = 'GL_EXT_texture_compression_rgtc'
_p.unpack_constants( """GL_COMPRESSED_RED_RGTC1_EXT 0x8DBB
GL_COMPRESSED_SIGNED_RED_RGTC1_EXT 0x8DBC
GL_COMPRESSED_RED_GREEN_RGTC2_EXT 0x8DBD
GL_COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT 0x8DBE""", globals())


def glInitTextureCompressionRgtcEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )
