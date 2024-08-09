cd ..
git clone https://github.com/565353780/open3d-manage.git

cd open3d-manage
./setup.sh

sudo apt install gcc-multilib g++-multilib

cd ../structured-3d/structured_td/Lib/PyMesh/third_party
./build.py all

cd ..
mkdir build
cd build
cmake ..
make -j
# make tests

cd ..
./setup.py build
./setup.py install

pip install -U open3d opencv-python descartes \
  matplotlib shapely panda3d tqdm

pip install numpy==1.24.4
