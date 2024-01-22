# Requires mock --enable-network to build... A TON of build time downloading
# ~/.cache/bazel/ grows to 5.6GB to build, then 7.8GB once done (2.14.1)

# Fix "Empty %files file" debugsourcefiles.list... not sure why, possibly
# because sources are outside BUILDROOT (~/.cache/bazel)?
%define _debugsource_template %{nil}

# With 20 CPU threads and 32GB RAM (i9-13900H) ... make -j20 ... oomkiller
%ifarch x86_64
%define _smp_ncpus_max 10
%endif
# With 6 CPU cores (4xA53, 2xA73) and 4GB RAM  ... make -j6 ... oomkiller
%ifarch aarch64
%define _smp_ncpus_max 3
%endif

# Build x86_64 with all by default, to typically run on recent hardware
%bcond_without avx
%bcond_without avx2
%bcond_without fma
%bcond_without sse4_1
%bcond_without sse4_2
# Same for ARM, default for recent CPUs
%bcond_without armv82a

Summary: High-performance serving system for machine learning models
Name: tensorflow-model-server
Version: 2.14.1
Release: 1%{?dist}
License: ASL 2.0
URL: https://www.tensorflow.org/serving
Source0: https://github.com/tensorflow/serving/archive/refs/tags/%{version}/serving-%{version}.tar.gz
BuildRequires: bazel6
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libstdc++-devel
BuildRequires: git-core
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
# For the API?
#BuildRequires: python3-pip

%description
TensorFlow Serving is a flexible, high-performance serving system for machine
learning models, designed for production environments. It deals with the
inference aspect of machine learning, taking models after training and
managing their lifetimes, providing clients with versioned access via a
high-performance, reference-counted lookup table. TensorFlow Serving provides
out-of-the-box integration with TensorFlow models, but can be easily extended
to serve other types of models and data.


#package python
#Summary: TensorFlow Serving Python files
#Requires: #{name} = #{version}-#{release}

#description python
#TBD.


%prep
%setup -q -n serving-%{version}


%build

# We want to limit the max number of parallel jobs (see above)
_SMP_MFLAGS=%{_smp_mflags}
JOBS=${_SMP_MFLAGS#-j}
# Try to keep close to tensorflow_serving/tools/docker/Dockerfile.devel
# * -Wno-stringop-truncation to avoid error from upb (tensorflow #39467)
# * Fetching repository @org_boost; Updating submodules recursively
#   ^ Times out after 609s so add --experimental_scale_timeouts=5.0
TF_SERVING_BAZEL_OPTIONS="-c opt \
%ifarch x86_64
%if %{with avx}
--copt=-mavx \
%endif
%if %{with avx2}
--copt=-mavx2 \
%endif
%if %{with fma}
--copt=-mfma \
%endif
%if %{with sse4_1}
--copt=-msse4.1 \
%endif
%if %{with sse4_2}
--copt=-msse4.2 \
%endif
%endif
%ifarch aarch64
%if %{with armv82a}
--copt=-march=armv8.2-a \
%endif
%endif
--copt=-Wno-stringop-truncation \
--jobs=${JOBS} \
--experimental_scale_timeouts=5.0"
# See .bazelrc
# Don't use --config=release since it adds only x86_64 specific avx and sse4.1
TF_SERVING_BUILD_OPTIONS=""

# Build TensorFlow Serving
bazel build --color=no --curses=yes \
  ${TF_SERVING_BAZEL_OPTIONS} \
  --verbose_failures \
  --output_filter=DONT_MATCH_ANYTHING \
  ${TF_SERVING_BUILD_OPTIONS} \
  tensorflow_serving/model_servers:tensorflow_model_server

# Build TensorFlow Serving API
bazel build --color=no --curses=yes \
  ${TF_SERVING_BAZEL_OPTIONS} \
  --verbose_failures \
  --output_filter=DONT_MATCH_ANYTHING \
  ${TF_SERVING_BUILD_OPTIONS} \
  tensorflow_serving/tools/pip_package:build_pip_package


%install
rm -rf %{buildroot}
install -D -m 0755 \
  bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server \
  %{buildroot}%{_bindir}/tensorflow_model_server


%files
%license LICENSE
%doc AUTHORS CONTRIBUTING.md README.md RELEASE.md
%{_bindir}/tensorflow_model_server

#files python
#...


%changelog
* Tue Jan 16 2024 Matthias Saou <matthias@saou.eu> 2.14.1-1
- Initial RPM release.

