import numcodecs
import zarr, shutil
import numpy as np
import pathlib
import os


class CSI_DATASET:
    def __init__(
        self, path=None, mode="a", chunk_first_dim=150, override=False, store=None
    ):
        assert store != None or path != None
        if store != None:
            self.root_group = zarr.open_group(store, mode=mode)
        else:
            self.root_group = zarr.open_group(zarr.DirectoryStore(path), mode=mode)
            if isinstance(path, pathlib.Path):
                path = path.as_posix()
            self.rootpath = path
            if override and os.path.exists(path):
                self.remove_data()
            print(f"CSI_DATAROOT:{path}")

        for k, v in {
            "raw": (3, 3, 114, 2),
            "amp": (3, 3, 114),
            "phase_diff": (2, 3, 114),
            "status": (),
        }.items():
            if k in self.root_group.array_keys():
                setattr(self, "array_" + k, self.root_group[k])

            else:
                if k == "status":
                    setattr(
                        self,
                        "array_" + k,
                        self.root_group.create_dataset(
                            k,
                            shape=(0),
                            chunks=(chunk_first_dim*100),
                            dtype=object,
                            object_codec=numcodecs.JSON(),
                            # compressor=None,
                        ),
                    )
                else:

                    setattr(
                        self,
                        "array_" + k,
                        self.root_group.create_dataset(
                            k,
                            shape=(0, *v),
                            chunks=(chunk_first_dim, *v),
                            dtype=np.float32,
                            # compressor=None,
                        ),
                    )

    def remove_data(self):

        shutil.rmtree(self.rootpath)
