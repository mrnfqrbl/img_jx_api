from typing import Any, Dict


class MetadataTranslator:
    # 定义中英键映射作为类变量
    TRANSLATION_MAP = {
        'file_info': '文件信息',
        'stable_diffusion_metadata': '稳定扩散(stable_diffusion)或novelai元数据',
        'filename': '文件名',
        'filesize': '文件大小',
        'image_width': '图像宽度',
        'image_height': '图像高度',
        'format': '文件格式',
        # 对 stable_diffusion_metadata_comment_parsed 中的字段做映射
        'prompt': '提示词',
        'steps': '步骤',
        'height': '高度',
        'width': '宽度',
        'scale': '缩放',
        'uncond_scale': '无条件缩放',
        'cfg_rescale': '配置重缩放',
        'seed': '种子',
        'n_samples': '样本数',
        'hide_debug_overlay': '隐藏调试层叠',
        'noise_schedule': '噪声计划',
        'legacy_v3_extend': '遗留v3扩展',
        'reference_information_extracted_multiple': '提取的参考信息',
        'reference_strength_multiple': '参考强度',
        'sampler': '采样器',
        'controlnet_strength': '控制网强度',
        'controlnet_model': '控制网模型',
        'dynamic_thresholding': '动态阈值',
        'dynamic_thresholding_percentile': '动态阈值百分比',
        'dynamic_thresholding_mimic_scale': '动态阈值模拟比例',
        'sm': 'SM',
        'sm_dyn': 'SM动态',
        'skip_cfg_above_sigma': '跳过配置高于Sigma',
        'skip_cfg_below_sigma': '跳过配置低于Sigma',
        'lora_unet_weights': 'Lora UNet 权重',
        'lora_clip_weights': 'Lora CLIP 权重',
        'deliberate_euler_ancestral_bug': '故意的欧拉祖先错误',
        'prefer_brownian': '偏好布朗运动',
        'cfg_sched_eligibility': '配置调度资格',
        'explike_fine_detail': '探索细节',
        'minimize_sigma_inf': '最小化Sigma Inf',
        'uncond_per_vibe': '无条件每个振动',
        'wonky_vibe_correlation': '怪异的振动相关性',
        'version': '版本',
        'uc': '负面',
        'request_type': '请求类型',
        'signed_hash': '签名哈希',
        # 新的字段映射
        'Description': '描述',
        'Software': '软件',
        'Source': '来源',
        'Generation time': '生成时间',
        'Comment': '生成信息',
        'keyword': '关键字',
        'text': '文本',
        'Title': '标题'
    }

    @staticmethod
    def translate_value(value: Any) -> Any:
        """将字符串值中的预设内容翻译为中文"""
        if isinstance(value, str):
            for eng, ch in MetadataTranslator.TRANSLATION_MAP.items():
                if eng in value:
                    value = value.replace(eng, ch)
        return value

    @staticmethod
    def translate_to_chinese(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """将元数据中的部分字段翻译为中文，保持值不变"""
        translated_metadata = {}

        # 遍历元数据并翻译字段名
        for key, value in metadata.items():
            translated_key = MetadataTranslator.TRANSLATION_MAP.get(key, key)  # 使用映射中的中文字段名
            if isinstance(value, dict):
                # 如果值是字典类型，递归调用翻译方法
                value = MetadataTranslator.translate_to_chinese(value)
            elif isinstance(value, list):
                # 如果值是列表类型，递归翻译列表中的字典
                value = [MetadataTranslator.translate_to_chinese(item) if isinstance(item, dict) else MetadataTranslator.translate_value(item) for item in value]
            else:
                # 如果值是字符串类型，尝试替换预设值
                value = MetadataTranslator.translate_value(value)

            # 保留原始数据结构，且翻译后的字段名赋值
            translated_metadata[translated_key] = value

        return translated_metadata



if __name__ == "__main__":
    a = {
        "file_info": {
            "filename": "D:\\xm\\img-jx\\input\\3.png",
            "filesize": "1.64 MB",
            "image_width": 832,
            "image_height": 1216,
            "format": "PNG"
        },
        "stable_diffusion_metadata": [
            {
                "keyword": "Software",
                "text": "NovelAI"
            },
            {
                "keyword": "Source",
                "text": "Stable Diffusion XL 7BCCAA2C"
            },
            {
                "keyword": "Generation_time",
                "text": "1.4280281770043075"
            },
            {
                "keyword": "Comment",
                "text": {
                    "prompt": "Nachoneko,artist: ciloranko, [Artist: Sho_(sho_LWLW)], [Artist: baku-p], [Artist: Tsubasa_tsubasa],artist:ciloranko , [artist:sho_(sho_lwlw)], [[artist:tianliang_duohe_fangdongye]],[[[[[[artist:kani_biimu]]]]]],[artist:baku-p], [artist:aki99],[[artist:as109]], [[artist:rhasta]], {{best quality}},gray hair, cat ears, white stockings,  {no underwear}},amazing quality, very aesthetic, absurdres,A girl, solo, loli, White socks,sneakers,Chinese cultivation battle, martial arts, Taoist magic, sword fighting, mystical energy, glowing spiritual aura, ancient Chinese landscape, ethereal fog, flying through the air, powerful energy blasts, elemental forces, graceful movements, intense combat, traditional robes, dramatic atmosphere, magical sword strikes, best quality, amazing quality, very aesthetic, absurdres",
                    "steps": 28,
                    "height": 1216,
                    "width": 832,
                    "scale": 5.5,
                    "uncond_scale": 0.0,
                    "cfg_rescale": 0.0,
                    "seed": 4229296041,
                    "n_samples": 1,
                    "hide_debug_overlay": False,
                    "noise_schedule": "karras",
                    "legacy_v3_extend": False,
                    "reference_information_extracted_multiple": [],
                    "reference_strength_multiple": [],
                    "sampler": "k_euler_ancestral",
                    "controlnet_strength": 1.0,
                    "controlnet_model": None,
                    "dynamic_thresholding": False,
                    "dynamic_thresholding_percentile": 0.999,
                    "dynamic_thresholding_mimic_scale": 10.0,
                    "sm": False,
                    "sm_dyn": False,
                    "skip_cfg_above_sigma": None,
                    "skip_cfg_below_sigma": 0.0,
                    "lora_unet_weights": None,
                    "lora_clip_weights": None,
                    "deliberate_euler_ancestral_bug": False,
                    "prefer_brownian": True,
                    "cfg_sched_eligibility": "enable_for_post_summer_samplers",
                    "explike_fine_detail": False,
                    "minimize_sigma_inf": False,
                    "uncond_per_vibe": True,
                    "wonky_vibe_correlation": True,
                    "version": 1,
                    "uc": "nsfw, lowres, jpeg artifacts, worst quality, watermark, blurry, very displeasing,  {{{shoe}}}{{Heterochromia}},{{Bondage}}, {{Bound}}, {{Leg Ring}},penis, male genitalia,{{{Convenient review}}},{{Objects blocking characters}}, objects,{{Chaos Tentacles}}, {{Chaos Slime}},{{Wrong human limbs}}，Remove logos, no watermarks, no text, no signatures, no copyright marks, no branding, avoid unnecessary objects, no cluttered backgrounds, no visible logos or labels, no exaggerated facial expressions, no cartoonish style,walk",
                    "request_type": "PromptGenerateRequest",
                    "signed_hash": "OI/k5GYgAhq+EN5Yl0SnyyQxfLSanmbQgigw9u0DD/Y4kgurt13Hrl0TyZGdiwlADaB1/BCRBJQctxnFFGWGCQ=="
                }
            },
            {
                "keyword": "Title",
                "text": "AI generated image"
            },
            {
                "keyword": "Description",
                "text": "Nachoneko,artist: ciloranko, [Artist: Sho_(sho_LWLW)], [Artist: baku-p], [Artist: Tsubasa_tsubasa],artist:ciloranko , [artist:sho_(sho_lwlw)], [[artist:tianliang_duohe_fangdongye]],[[[[[[artist:kani_biimu]]]]]],[artist:baku-p], [artist:aki99],[[artist:as109]], [[artist:rhasta]], {{best quality}},gray hair, cat ears, white stockings,  {no underwear}},amazing quality, very aesthetic, absurdres,A girl, solo, loli, White socks,sneakers,Chinese cultivation battle, martial arts, Taoist magic, sword fighting, mystical energy, glowing spiritual aura, ancient Chinese landscape, ethereal fog, flying through the air, powerful energy blasts, elemental forces, graceful movements, intense combat, traditional robes, dramatic atmosphere, magical sword strikes, best quality, amazing quality, very aesthetic, absurdres"
            }
        ]
    }

    new_data=MetadataTranslator.translate_to_chinese(a)
    print(MetadataTranslator.translate_to_chinese(a))