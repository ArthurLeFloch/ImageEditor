let url = `http://${location.hostname}:3000`;
if (import.meta.env.PROD) {
    url = "/server";
}

export async function _fetchImage(endpoint, image, onResolve, params = {}) {
    try {
        const formData = new FormData();
        formData.append('image', image);
        for (const [key, value] of Object.entries(params)) {
            formData.append(key, value);
        }

        const response = await fetch(`${url}/${endpoint}`, {
            method: 'POST', body: formData, headers: {'enctype': 'multipart/form-data'},
        });
        onResolve(await response.blob());
    } catch (error) {
        console.error('Error fetching image:', error);
    }
}


export function useActionDetailsProps(props) {
    return (endpoint, params) => _fetchImage(endpoint, props.getFile(), props.setFile, params);
}