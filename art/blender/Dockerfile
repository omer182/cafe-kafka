# Headless Blender 4.2 LTS for rendering sprites. Cycles runs on CPU; EEVEE runs
# on Mesa's software OpenGL (llvmpipe) through EGL, so no GPU is needed.
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl xz-utils \
      libx11-6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 libsm6 libgl1 libegl1 libglu1-mesa libgomp1 \
      libgl1-mesa-dri libegl-mesa0 libglx-mesa0 \
 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz | tar -xJ -C /opt \
 && ln -s /opt/blender-4.2.3-linux-x64/blender /usr/local/bin/blender
# VRM add-on (MIT), for importing VRoid / VRM characters
COPY addon.zip /tmp/vrm.zip
RUN blender -b --factory-startup --online-mode --python-expr "import bpy; bpy.ops.extensions.package_install_files(repo='user_default', filepath='/tmp/vrm.zip', enable_on_install=True); bpy.ops.wm.save_userpref()" \
 && rm /tmp/vrm.zip
ENV HOME=/root
WORKDIR /work
ENTRYPOINT ["blender", "-b"]
